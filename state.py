from copy import deepcopy

from expressions import IsType, IsGroupElement

class State:
        
    def __init__(self, variables={}, assumptions={}, goals={}):
        self.done = False
        self.variables = variables
        self.assumptions = assumptions
        self.goals = goals

        self.past_actions = []

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """ 
        Hash uses only past_actions information (disregards variables, assumptions, goals) for qtable 
        """
        return hash(tuple(self.past_actions))

    def __repr__(self):
        return "{} with past actions {}".format(self.__class__.__name__, [a for a,b in self.past_actions])
    
    # def __str__(self):
    #     return self.__repr__()
        # s = "New State \n"

        # s = "\tVariables\n"
        # for name, value in self.variables.items():
        #     s+= "\t\t{}: {}\n".format(name, value)

        # s+= "\tAssumptions\n"
        # for name, value in self.assumptions.items():
        #     s+= "\t\t{}: {}\n".format(name, value)

        # s+= "\tGoals\n"
        # for name, value in self.goals.items():
        #     s+= "\t\t{}: {}\n".format(name, value)

        # return s

    def add_variables(self, dic):
        """ Concatenate the passed-in dictionary with the existing dictionary """
        self.variables.update(dic)

    def add_assumptions(self, dic):
        """ Concatenate the passed-in dictionary with the existing dictionary """
        self.assumptions.update(dic)

    def add_goals(self, dic):
        """ Concatenate the passed-in dictionary with the existing dictionary """
        self.goals.update(dic) 

    def get_copy(self):
        """ 
        Need a copy for indexing in python dictionary
        Otherwise the state changes, and the key in the dictionary changes with it, and so it is in the wrong hashbucket
        """
        return deepcopy(self)





