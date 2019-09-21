import os
import math
import gym
import numpy as np

from debug_settings import *

from coqtypes import *
from actions import *
from coqinterface import CoqInterface
from state import State

PATH = os.path.dirname(os.path.abspath(__file__))+"/coq/"

class TheoremProvingEnvironment(gym.Env):
    """
    Reward:
        Gives reward when theorem proved.
        Gives penalty when coq throws an error.

    Starting State:
        All the variables, assumptions, and goal of the theorem.

    State: 
        All the variables, assumptions, and goal of the theorem...
        ...and proof actions taken.

    Episode Termination:
        When coq outputs "No more subgoals."
    """

    def __init__(self, thm):
        """ 
        Initialize environment using variables, assumptions, and goals of the theorem 
        """

        # self.seed(0) # set up randomization

        self.thm = thm
        self.state = None
        self.coqtop = None

        self.reset()

    def step(self, action):
        """
        (1) Send whatever the action is to Coq
        (2) Update environment's state
        """
        # hacky fix -- change later
        if action == Undo: # Undo doesn't come called like Undo(), but others do
            action = action(self.state)

        # Send to coq
        try:
            response = self.coqtop.sendone(str(action))

            if PRINT_COQ_RESPONSES: print("SENDING TO COQ: \n\t<"+str(action)+">\n")
            if PRINT_COQ_RESPONSES: print("RESPONSE FROM COQ: \n\t<"+response.strip().replace("\r\n", "\n\t")+">\n")
            
            if PRINT_ACTIONS: print("Successfully took action:", action.__repr__())
        
        except (CoqError, UndoError):
            if PRINT_ACTIONS: print("Un-successfully took action:", action.__repr__())
            
            return self.state, -10, self.state.done

        # Update environment's state
        action.update_environment_state(self.state, response)
        if not isinstance(action, Undo):
            self.state.past_actions.append((action.get_copy(), action.get_undo_number(response)))

        # Determine reward
        if self.state.done:
            reward = 1 # reward for finishing proof
        elif isinstance(action, Undo):
            reward = -1000 # big negative reward for using undo (it usually moves us back in proof)
        else:
            reward = 0

        return self.state, reward, self.state.done

    
    def reset(self):
        """ 
        Reset state of environment.
        Starts up coqtop, and loads in theorem.
        """

        # create new coq interface (if one is already running, kill it first)
        if not self.coqtop:
            self.coqtop = CoqInterface(env=self) # set up coq interactivity
        else:
            self.coqtop.exit()
            self.coqtop = CoqInterface(env=self)

        theorem = self.thm(env=self)

        self.state = State(variables = {}, assumptions = {}, goals = {})

        action = AddVariables(theorem.get_variables())
        self.step(action)

        action = AddAssumptions(theorem.get_assumptions())
        self.step(action)

        action = AddGoals(theorem.get_goals())
        self.step(action)

        action = StartProvingTheorem("cancellation_law", assumptions=self.state.assumptions, goal=self.state.goals["finalgoal"])
        self.step(action)

        self.action_space = theorem.get_necessary_actions() # load in all necessary actions to prove theorem
                                                      # in the future, should be universal set of actions, not theorem-dependent

        return self.state
