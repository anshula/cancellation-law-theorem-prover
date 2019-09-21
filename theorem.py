import numpy as np

from coqtypes import Group, Variable
from expressions import IsGroupElement, IsEqual, Product
from actions import *

class Theorem:
    """
    A Theorem is passed in to the Environment right before an Agent starts to try to prove it.
    """
    pass

class CancellationLaw(Theorem):
    def __init__(self, env):
        self.env = env

    def get_variables(self):
        return {
            "x0":Variable("x0"),
            "x1":Variable("x1"),
            "x2":Variable("x2"),
            "G" :Group("G")
        }

    def get_assumptions(self):
        var = self.get_variables()

        return {
            "H1": IsGroupElement(var["x0"], var["G"]), 
            "H2": IsGroupElement(var["x1"], var["G"]), 
            "H3": IsGroupElement(var["x2"], var["G"]),
            "H4": IsEqual(Product(var["x0"], var["x1"], operation=var["G"].operation),
                          Product(var["x0"], var["x2"], operation=var["G"].operation))
        }

    def get_goals(self):
        var = self.get_variables()

        return {
            "finalgoal": IsEqual(var["x1"], var["x2"])
        }

    def get_necessary_actions(self):
        state = self.env.state

        return np.array([LeftMultiplyByInverse(in_eqn="H4", out_eqn="H5", expr="x0", state=state),
                    ApplyLeftInverseProperty(in_eqn = "H5", group = "G", side = "left"), 
                    ApplyLeftInverseProperty(in_eqn = "H5", group = "G", side = "right"), 
                    ApplyIdentityProperty(in_eqn = "H5", group = "G", side = "left"), 
                    ApplyIdentityProperty(in_eqn = "H5", group = "G", side = "right"), 
                    ApplyAssociativity(in_eqn = "H5", group = "G", side = "left"), 
                    ApplyAssociativity(in_eqn = "H5", group = "G", side = "right"),
                    Undo # sometimes creates infinite loop in agent.evaluate() because there's no way to penalize Undo when qtable stays stagnant
                    ])

