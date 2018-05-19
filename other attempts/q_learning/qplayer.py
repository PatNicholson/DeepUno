"""
Player that uses q-learning. 
"""

from objects import *
import pandas as pd
import numpy as np
import random 


class Qplayer(Player):
    def __init__(self):
        Player.__init__(self,game,name)
        self.Q = {}
        self.last_state = None
        self.last_action = None
        self.learning_rate = .7
        self.discount = .9
        self.epsilon = .9
        self.learning = True


    def get_action(self, state):
        # determine which action to do 
        if state in self.Q and np.random.uniform(0,1) < self.epsilon:
            action = max(self.Q[state], key = self.Q[state].get)
        else:
            action = np.random.choice(self.all_possible_cards())
            self.discard(action)
            if state not in self.Q:
                self.Q[state] = {}
            self.Q[state][action] = 0

        self.last_state = state
        self.last_action = action

        return action

    def update(self,new_state,reward):
    	# approximate Q function at time t, denoted Qt with a value update at (s,a):
    	# Q_t+1 (s, a) = Q_t(s,a) + alpha * [r_t + gamma * max_a( Q_t(s_t+1,a)−Q(s_t,a) )] 
    	# alpha = learning_rate, gamma = discount factor, 
        if self.learning:
            old = self.Q[self.last_state][self.last_action]

            if new_state in self._Q:
                new = self.discount * self.Q[new_state][max(self.Q[new_state], key=self.Q[new_state].get)]
            else:
                new = 0

            self.Q[self.last_state][self.last_action] = (1-self.learning_rate)*old + self.learning_rate*(reward+new)

    def get_optimal_strategy(self):
        #get optimal card to discard
        df = pd.DataFrame(self.Q).transpose()
        print(df)
        #df['optimal'] = df.apply(lambda x :  if x['draw'] >= x['discard'] else 'discard', axis=1)
        return df
