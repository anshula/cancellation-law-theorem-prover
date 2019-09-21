import random
import numpy as np

from debug_settings import *

from environment import TheoremProvingEnvironment
from theorem import CancellationLaw
from agent import Agent

if SET_RANDOM_SEED: 
    random.seed(5)
    np.random.seed(5)

# ----------------------------------------------------------------------------------
# Set up environment with a start state including variables, assumptions, and goal
# ----------------------------------------------------------------------------------
env = TheoremProvingEnvironment(thm=CancellationLaw)

# ----------------------------------------------------------------------------------
# Evaluate agent when q-table is empty (should be pretty bad)
# ----------------------------------------------------------------------------------
a = Agent(env)
episodes, total_epochs, total_penalties = a.evaluate(episodes=3)
print(f"BEFORE TRAINING:")
print(f"\tAverage timesteps per episode: {total_epochs / episodes}")
print(f"\tAverage penalties per episode: {total_penalties / episodes}")

# # ----------------------------------------------------------------------------------
# # Train agent by filling out the q-table
# # ----------------------------------------------------------------------------------

print("\nTRAINING...")
a.train(episodes=5)
print("Training finished.\n")
# print(a.qtable)

# # ----------------------------------------------------------------------------------
# # Evaluate how well agent was trained by evaluating how well it performs with new qtable
# # ----------------------------------------------------------------------------------
episodes, total_epochs, total_penalties = a.evaluate(episodes=3)
print(f"AFTER TRAINING:")
print(f"\tAverage timesteps per episode: {total_epochs / episodes}")
print(f"\tAverage penalties per episode: {total_penalties / episodes}")


