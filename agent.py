import numpy as np

from qtable import QTable
from actions import *

class Agent:
    """
    Uses qlearning to train itself within an environment.

    q_table:
        q_table is a dynamically generated dictionary of states x actions
        q_table[state][action] gives probability agent should take that action

    """
    def __init__(self, env):
        self.env = env
        self.qtable = QTable(env.action_space)

    def train(self, episodes=5, alpha=0.1, gamma=0.6, epsilon=0.1):
        """
        Train agent using qlearning.
        Code inspired by: https://learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/
        """

        env = self.env
        qtable = self.qtable

        # Run episodes
        for _ in range(episodes):
            state = env.reset()
            epochs, penalties, reward, = 0, 0, 0
            
            while not env.state.done:
                # ------------------------------------
                # Choose to explore or exploit
                # ------------------------------------
                if np.random.uniform(0, 1) < epsilon: # Explore action space
                    action = qtable.get_random_action() 
                else: # Exploit the action space
                    action = qtable.get_recommended_action(state) 

                next_state, reward, done = env.step(action) # will return error and undo, if unsuccessful
                # ------------------------------------
                # See if we're done with the proof
                # ------------------------------------
                env.step(VerifyGoalReached()) # will return error and undo, if unsuccessful

                # ------------------------------------
                # Update the qtable
                # ------------------------------------
                qtable.update(state, next_state, action, reward, alpha, gamma)

                if reward < 0:
                    penalties += 1

                state = next_state
                epochs += 1

            # print("Proof generated:", env.state.past_actions)
            # for a in env.state.past_actions:
            #     print(a.to_coq())

        # print(self.qtable)

    def evaluate(self, episodes=5, empty_q_table=False):
        """
        Evaluate agent's performance after Q-learning
        Code inspired by: https://learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/
        
        If empty_q_table is true, then instead of exploiting best action, the agent chooses action randomly
            And it chooses WITHOUT undo, which can slow down proof progress

            So setting empty_q_table=True often just speeds up evaluation by not allowing agent to Undo past actions
            (If we allow Undoing at random, the agent often takes twice as long)
        """

        env = self.env
        qtable = self.qtable

        total_epochs, total_penalties = 0, 0

        for _ in range(episodes):
            state = env.reset()
            epochs, penalties, reward = 0, 0, 0
                        
            while not env.state.done:
                # ------------------------------------
                # Exploit highest-rated action on q-table
                # ------------------------------------
                if empty_q_table: #if the q table is empty, it's equivalent to randomly choosing.  but should not use Undo action, because it will get overused
                    action = qtable.get_random_action(undo=False)
                else: #otherwise, use the q table to exploit   
                    action = qtable.get_recommended_action(state) 
                state, reward, done = env.step(action)


                # ------------------------------------
                # See if we're done with the proof
                # ------------------------------------
                env.step(VerifyGoalReached()) # will return error and undo, if unsuccessful

                if reward < 0:
                    penalties += 1

                epochs += 1

            total_penalties += penalties
            total_epochs += epochs

        return episodes, total_epochs, total_penalties
