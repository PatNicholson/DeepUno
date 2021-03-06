"""
Control AI. Plays randomly.
"""

from objects import *
import random
import numpy as np

from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate

random.seed()

class reinforce_nn_fi(Player):
    def __init__(self, game, name, model = None):
        Player.__init__(self,game,name)
        self.colors = ["red", "blue", "green", "yellow",None]
        self.color_counts = [0]*5
        self.value_counts = [0]*11
        self.flag_counts = [0]*6
        self.model = model
        self.pastplays = []

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0
    
    def train(self,winner): #training with 0-1 labels currently
        if len(self.pastplays) == 0:
            return
        labels = np.zeros((len(self.pastplays), 1))
        features = np.asarray(self.pastplays, dtype=np.float32)
        if winner:
            labels = np.ones((len(self.pastplays), 1))
        self.model.fit(features,labels,verbose=0)
        self.pastplays = []

    def play(self):
        #update counts for opponent's hand
        self.update_totals()
        
        if self.discard_or_draw():
            drawn_card = self.draw()
            color_idx = self.colors.index(drawn_card.color)
            self.color_counts[color_idx] -= 1
            self.value_counts[drawn_card.value] -= 1
            self.flag_counts[drawn_card.flag] -= 1
            return [1,drawn_card,self.game.wild_color]
        else:
            possible_discards = self.all_possible_cards()
            i, wild_color, prob = self.select_discard(possible_discards)
            discard_card = possible_discards[i]
            return [0,self.discard(discard_card),wild_color]
        
    def select_discard(self,possible_discards):
        hand_colors = [0]*5
        hand_values = [0]*11
        hand_flags = [0]*6
        for c in self.hand.cards:
            color_idx = self.colors.index(c.color)
            hand_colors[color_idx] += 1
            hand_values[c.value] += 1
            hand_flags[c.flag] += 1
        len_opp_hand = len(self.game.player2.hand.cards)
        if self.game.player2.name == self.name:
            len_opp_hand = len(self.game.player1.hand.cards)
         
        best_idx = 0
        best_val = -100000
        best_wild = None
        best_vector = []
        for i in range(len(possible_discards)):
            d = possible_discards[i]
            wild_color = None
            if d.flag >= 4:
                wild_color = self.select_wild_color()
            
            discard_colors = [0]*5
            hand_colors2 = hand_colors[:]
            color_idx = self.colors.index(d.color)
            hand_colors2[color_idx] -= 1
            discard_colors[color_idx] += 1
            
            discard_values = [0]*11
            hand_values2 = hand_values[:]
            hand_values2[d.value] -= 1
            discard_values[d.value] += 1
            
            discard_flags = [0]*6
            hand_flags2 = hand_flags[:]
            hand_flags2[d.flag] -= 1
            discard_flags[d.flag] += 1
            
            color_dist = [x/float(sum(self.color_counts)) for x in self.color_counts[:]]
            value_dist = [x/float(sum(self.value_counts)) for x in self.value_counts[:]]
            flag_dist = [x/float(sum(self.flag_counts)) for x in self.flag_counts[:]]
            
            vector = hand_colors2 + hand_values2 + hand_flags2 + color_dist + \
                value_dist + flag_dist + [len_opp_hand] + discard_colors + discard_values + discard_flags
            val = self.model.predict(np.array(vector, dtype=np.float32).reshape(1,len(vector)))
            if val > best_val:
                best_idx = i
                best_val = val
                best_wild = wild_color
                best_vector = vector
        if best_val > -100000:
            self.pastplays.append(best_vector)
        return best_idx, best_wild, best_val
    
    #updates counts of what cards the player hasn't seen in their hand or discarded  
    def update_totals(self):
        self.color_counts = [0]*5
        self.value_counts = [0]*11
        self.flag_counts = [0]*6
        
        #accumulate counts of cards in opponent's hand
        opp_player = self.game.player2
        if opp_player.name == self.name:
            opp_player = self.game.player1
        for i in range(len(opp_player.hand.cards)):
            color_idx = self.colors.index(opp_player.hand.cards[i].color)
            self.color_counts[color_idx] += 1
            self.value_counts[opp_player.hand.cards[i].value] += 1
            self.flag_counts[opp_player.hand.cards[i].flag] += 1
                
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

    def say_uno(self):
        self.game.uno(self)
