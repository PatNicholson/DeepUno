"""
Neural network AI
"""
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import numpy as np
from objects import *
import random


class simple_nn(Player):
    def __init__(self, game, name, model = None, training = False):
        Player.__init__(self,game,name)
        self.model = model
        self.weights = self.game.deck.get_weights()
        self.training = training

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0
    
    def select_wild_color(self):
        yellow = 0
        red = 0
        blue = 0
        green = 0
        for c in self.hand.cards:
            if c.color == "yellow":
                yellow += 1
            elif c.color == "red":
                red += 1
            elif c.color == "blue":
                blue += 1
            elif c.color == "green":
                green += 1
        best_option = (max((yellow,"yellow"),(red,"red"),(blue,"blue"),
            (green,"green")))[1]
        return best_option

    def play(self):
        if self.discard_or_draw():
            return [1,self.draw(),None]
        else:
            wild_color = None
            possible_discards = [c.index for c in self.all_possible_cards()]
            hand_weights = np.zeros(108)
            hand_weights[possible_discards] = self.weights[possible_discards]


            probs = self.model.predict(hand_weights.T)

            discard_card = self.all_possible_cards()[np.argmax(probs[possible_discards])]

            if discard_card.flag >= 4: #if wild, randomly select new color
                wild_color = self.select_wild_color()
                
            if self.training:
                self.model.fit(hand_weights, probs, nb_epoch=1, verbose=0)

            return [0,self.discard(discard_card),wild_color]


    def say_uno(self):
        self.game.uno(self)
