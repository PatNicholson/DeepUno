"""
Player that uses q-learning for neural network 
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
from objects import *
from qplayer import *
import numpy as np
import tensorflow as tf
import pandas as pd

class Dqn_player(Qplayer):
    def __init__(self):
        Player.__init__(self,game,name)
        self.last_state = None
        self.last_action = None
        self.learning = True
        self.learning_rate = .1
        self.discount = .1
        self.epsilon = .9

        # Create Model
        model = Sequential()

        model.add(Dense(self.game.deck.size_of_deck(), init='lecun_uniform', input_shape=(deck.size_of_deck(),)))
        model.add(Activation('relu'))

        model.add(Dense(self.deck.size_of_deck() * 2, init='lecun_uniform'))
        model.add(Activation('relu'))

        model.add(Dense(deck.size_of_deck(), init='lecun_uniform'))
        model.add(Activation('linear'))

        rms = RMSprop()
        model.compile(loss='mse', optimizer=rms)

        self._model = model


    def get_action(self, state):
        rewards = self._model.predict([np.array([state])], batch_size=1)

        if np.random.uniform(0,1) < self._epsilon:
            if rewards[0][0] > rewards[0][1]:
                action = 'draw'
            else:
                action = 'discard'
        else:
            action = "discard" + str(discard_card.value) + discard_card.color + discard_card.flag

        self.last_state = state
        self.last_action = action
        self.last_target = rewards


        return action

    def update(self,new_state,reward):
        if self.learning:
            rewards = self._model.predict([np.array([new_state])], batch_size=1)
            maxQ = rewards[0][0] if rewards[0][0] > rewards[0][1] else rewards[0][1]
            new = self._discount * maxQ

            # TODO: fix according to card type
            if self.last_action == "draw":
                self.last_target[0][0] = reward+new
            else:
                self.last_target[0][1] = reward+new

            # Update model
            self._model.fit(np.array([self.last_state]), self.last_target, batch_size=1, nb_epoch=1, verbose=0)

    def get_optimal_strategy(self):

        index = []
        for x in range(0,21):
            for y in range(1,11):
                index.append((x,y))

        df = pd.DataFrame(index = index, columns = ['draw', 'discard'])

        for ind in index:
            outcome = self._model.predict([np.array([ind])], batch_size=1)
            df.loc[ind, 'draw'] = outcome[0][0]
            df.loc[ind, 'discard'] = outcome[0][1]


        df['optimal'] = df.apply(lambda x : 'draw' if x['draw'] >= x['discard'] else 'discard', axis=1)
        return df