"""
Neural network AI
version I am messing around with
"""
import numpy as np
from objects import *
import random

from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate


class simple_nn(Player):
    def __init__(self, game, name, model = None, training = False):
        Player.__init__(self,game,name)
        self.model = model
        self.training = training

    def train(self):
        return model

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

            # getting the cards in hand
            colors = ["red", "blue", "green", "yellow", None]
            hand_cards = np.zeros((108, 4))
            possible_discards = []
            for card in self.all_possible_cards():
                if card.flag >= 4:
                    wild_color = self.select_wild_color()
                    hand_cards[card.index] = [card.index, card.value, colors.index(wild_color), card.flag]
                else:
                    hand_cards[card.index] = [card.index, card.value, colors.index(card.color), card.flag]
                possible_discards.append(card.index)

            # size of the opponent's hand
            opponent = self.game.player2
            if opponent.name == self.name:
                opponent = self.game.player1
            opp_hand_size = len(opponent.hand.cards)

            # size of discard pile and topmost card in the pile
            discard_size = len(self.game.discard_pile.cards)
            if discard_size > 0:
                card = self.game.discard_pile.cards[-1]
                top_card_discard_pile = np.array([card.index, card.value, colors.index(card.color), card.flag])

            # size of the deck 
            deck_size = self.game.deck.size_of_deck()

            # combine all features into one input
            features = np.hstack((hand_cards.flatten(), opp_hand_size , discard_size, top_card_discard_pile.flatten(), deck_size)).flatten()

            # get predictions
            probs = self.model.predict(features) 
            #probs = self.model.predict([hand_cards, len(opp_player.hand.cards)])
            
            discard_card = self.all_possible_cards()[np.argmax(probs[possible_discards])]

            if self.training:
                self.model.fit(features, probs, verbose=0)
                #self.model.fit([hand_cards, len(opp_player.hand.cards)], probs, verbose=0)

            return [0,self.discard(discard_card),wild_color]


    def say_uno(self):
        self.game.uno(self)
