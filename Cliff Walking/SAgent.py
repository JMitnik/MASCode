import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
import seaborn as sns

from Agent import Agent

ALPHA = 0.1
GAMMA = 1

def swap_tuple(input_tuple):
    """Why swap: Because numpy gets (row,col) coordinates corresponding to (y,x), so to use x,y, we need to swap that"""
    a, b = input_tuple
    return (b,a)

class SAgent(Agent):
    def __init__(self, env, nr_episodes, epsilon=0.2 ):
        super().__init__(env, epsilon)
        self.nr_episodes = nr_episodes
        
    def run(self):
        """ Does a run for x number of episodes. """
        for i in range(self.nr_episodes):
            self.curr_state = self.env.spawn_in_environment()
            
            while not self.terminated():
                curr_state = self.curr_state
                action_index = self.get_next_action(self.curr_state)

                next_state = self.get_next_state(action_index)
                action_index_next_state = self.get_next_action(next_state)

                self.update_q_table(action_index, next_state, action_index_next_state)
                self.update_state(next_state)

    def update_q_table(self, action_index, next_state, next_state_action):
        """ Updates the Q-table according to the SARSA-Learning Bellman's equation. """
        curr_q = self.q_table[swap_tuple(self.curr_state)][action_index]
        td_target = self.get_reward_for_state(next_state) + (GAMMA * self.q_table[swap_tuple(next_state)][next_state_action])
        td_delta = td_target - curr_q

        self.q_table[swap_tuple(self.curr_state)][action_index] += ALPHA * td_delta