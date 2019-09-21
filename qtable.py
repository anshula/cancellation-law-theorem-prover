import numpy as np
from actions import Undo

class QTable():
    """
    Wrapper class around q_table dictionary
    q_table[state][action] contains a value that is 
        higher if the action at that state might yield a high reward
        lower if the action at that state might yield a low reward
    """
    def __init__(self, action_space):
        self.q_table = {}
        self.action_space = action_space
        self.action_space_without_undo = [action for action in self.action_space if action is not Undo]
    def __str__(self):
        s = ""
        for state, dic in self.q_table.items():
            s+=str(state)
            s+="\n"
            for action, val in dic.items():
                s+="\t"+action.__repr__()+" : "+str(val)+"\n"
            s+="\n"
        return s

    def contains(self, state):
        return state in self.q_table

    def get_recommended_action(self, state):
        """
        Exploit.
        Chooses randomly among top-rated actions for a given state.
        """
        self.ensure_state_in_qtable(state) # to avoid key error

        max_val = max(self.q_table[state].values()) # get the max value in this space
        max_actions = [k for k,v in self.q_table[state].items() if v >= max_val] # get all the actions that have that value
        action = np.random.choice(max_actions)# choose randomly among those actions with max value

        return action

    def get_random_action(self, undo = True):
        """ 
        Explore.
        Chooses randomly among actions for a given state.

        Sometimes the undo method is not allowed (e.g. when the qtable is empty, before training)
            because if it is, agent will choose undo just as often as other actions
            and the proof is never completed
        But when when the q_table is full or training, the undo method is allowed
            because the undo method is penalized on the q_table so the agent doesn't overuse it
        """
        
        if not undo: # if undo isn't allowed, choose from actions without Undo
            action = np.random.choice(self.action_space_without_undo)
        else:
            action = np.random.choice(self.action_space)

        return action

    def ensure_state_in_qtable(self, state):
        """ If the state is not already in the qtable, add it in with all 0s for each action """
        if state not in self.q_table:
            self.q_table[state.get_copy()] = {action:0.0 for action in self.action_space}
            
    def update(self, state, next_state, action, reward, alpha, gamma):
        """ Update qtable based on reward from last action"""
        self.ensure_state_in_qtable(state) # to avoid key error
        self.ensure_state_in_qtable(next_state) # to avoid key error
        
        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values()) #get the maximum q_table reward value in next state
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        
        self.q_table[state][action] = new_value

