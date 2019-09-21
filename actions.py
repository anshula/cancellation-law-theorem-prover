from copy import deepcopy

from coqtypes import Variable
from expressions import IsEqual, Product
from errors import *


class Action:
    def __init__(self):
        pass

    def to_coq(self):
        return ". "

    def __str__(self):
        return self.to_coq()

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return self.__class__.__name__

    def update_environment_state(self, state, response):
        pass

    def get_undo_number(self, response):
        return self.to_coq().count('.') - response.count('Error')

    def get_copy(self):
        """ 
        Need a copy for storing in env.state.past_actions
        Because sometimes the to_coq() of an action is dependent on the state
        And we want to make sure even if the current state of the env is different
        The action remains the same action taken at that moment
        """
        return deepcopy(self)


class AddVariables(Action):
    def __init__(self, dic):
        self.dic = dic

    def to_coq(self):
        s = ""
        s += 'Add LoadPath "./coq". '
        s += "Require Import group. " # custom implementation of a group
        s += "Require Import Setoid. " # coq library required to only apply a property to first instance (e.g. only apply associativity to left side of eqn)
        s += "Section theorems. "
        s += "Variable U:Type. "
        for var in self.dic.values():
            s+= var.to_coq_declare()

        s += "Arguments S [U]. "
        s += "Arguments op [U] _ _. "
        s += "Arguments inv [U] _. "
        s += "Arguments op_inv_l [U] _. "
        s += "Arguments op_id_l [U] _. "
        s += "Arguments op_assoc[U]. "

        return s

    def update_environment_state(self, state, response):
        state.variables.update(self.dic)

class AddAssumptions(Action):
    def __init__(self, dic):
        self.dic = dic

    def to_coq(self):
        s = ""
        for name, assumption in self.dic.items():
            s+= "Let {} := {}. ".format(name, assumption.to_coq())
        return s

    def update_environment_state(self, state, response):
        state.assumptions.update(self.dic)

class AddGoals(Action):
    def __init__(self, dic):
        self.dic = dic

    def to_coq(self):
        s = ""
        for name, goal in self.dic.items():
            s+= "Let {} := {}. ".format(name, goal.to_coq())
        return s

    def update_environment_state(self, state, response):
        state.goals.update(self.dic)

class StartProvingTheorem(Action):
    def __init__(self, name, assumptions, goal):
        self.name = name
        self.assumptions = assumptions
        self.goal = goal

    def to_coq(self):
        # Theorem cancellation_law: H1 -> H2 -> H3 -> H4 -> x1 = x2. Proof.
        s = "Theorem {}: ".format(self.name)
        for assumption_name in self.assumptions.keys():
            s += assumption_name + " -> "
        s += self.goal.to_coq()
        s += ". "
        s += "Proof. "
        for assumption_name in self.assumptions.keys(): # introduce all dummy variables
            s+= "intros {}. ".format(assumption_name.replace("H","D"))
        return s

class LeftMultiply(Action):
    def __init__(self, in_eqn, out_eqn, expr, state):
        self.in_eqn = state.assumptions[in_eqn]
        self.out_eqn = out_eqn
        self.expr = state.variables[expr]

    def to_coq(self):
        return "assert (op G ({}) ({}) = op G ({}) ({})) as {}. f_equal. assumption.".format(self.expr, self.in_eqn.left.to_coq(), self.expr, self.in_eqn.right.to_coq(), self.out_eqn)

    def update_environment_state(self, state, response):
        eqn = IsEqual(Product(self.expr, self.in_eqn.left), Product(self.expr, self.in_eqn.right))
        dic = {self.out_eqn: eqn}
        state.assumptions.update(dic)

class LeftMultiplyByInverse(LeftMultiply):      
    def __init__(self, in_eqn, out_eqn, expr, state):
        self.in_eqn = state.assumptions[in_eqn]
        self.out_eqn = out_eqn
        self.expr = "inv G {}".format(state.variables[expr])
        
class ApplyGroupProperty(Action):
    def __init__(self, in_eqn, prop, side):
        self.in_eqn = in_eqn
        self.property = prop
        self.side = side
        self.assumption = True

    def to_coq(self):
        rewrite = "rewrite ({}) in {} at 1. ".format(self.property, self.in_eqn)
        if self.assumption:
            rewrite += "2:assumption." # resolve the 2nd subgoal (that the item is in the group) by assumption
        if self.side == "left":
            return rewrite
        # to apply property to right side: flip equation using symmetry, then flip back
        return "symmetry in {}. {} symmetry in {}.".format(self.in_eqn, rewrite, self.in_eqn)

class ApplyAssociativity(ApplyGroupProperty):
    def __init__(self, in_eqn, group, side):
        super().__init__(in_eqn, "op_assoc " + group, side)
        self.assumption = False

class ApplyLeftInverseProperty(ApplyGroupProperty):
    def __init__(self, in_eqn, group, side):
        super().__init__(in_eqn, "op_inv_l " + group, side)

class ApplyIdentityProperty(ApplyGroupProperty):
    def __init__(self, in_eqn, group, side):
        super().__init__(in_eqn, "op_id_l " + group, side)

class VerifyGoalReached(Action):
    def to_coq(self):
        return "assumption. Qed."

    def update_environment_state(self, state, response):
        if "No more subgoals" in response:
            state.done = True

class Undo(Action):
    def __init__(self, state):
        self.state = state

    def to_coq(self):
        num_undos = self.state.past_actions[-1][1]
        return "Undo. "*num_undos

    def update_environment_state(self, state, response):
        if state.past_actions:
            del state.past_actions[-1]

class Trivial(Action):
    def __init__(self):
        pass

    def to_coq(self):
        return "trivial. "
