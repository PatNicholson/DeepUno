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

class reinforce_nn_drawn(Player):
    def __init__(self, game, name, model = None, hand_size = 7):
        Player.__init__(self,game,name, hand_size)
        self.colors = ["red", "blue", "green", "yellow",None]
        self.color_counts = [0]*5
        self.value_counts = [0]*11
        self.flag_counts = [0]*6
        self.discard_len = 1000000 #ensure totals are updated at first play
        self.model = model
        self.pastplays = []
        self.opp_hand_len = 7
        self.update_label = False
        self.labels = []

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0
    
    def train(self,winner):
        #if self.update_label:
        #    opp = self.game.player2
        #    if self.game.player2.name == self.name:
        #        opp = self.game.player1
        #    #self.labels[len(self.labels)-1][0] += self.h(-1,opp.hand.cards)
        #    self.update_label = False
        if len(self.pastplays) == 0:
            return
        #print(self.labels)
        #sum_labels = 0
        #for i in range(len(self.labels)):
        #    sum_labels += self.labels[i][0]
        #print(sum_labels)
        #print('-------------------')
        
        np_labels = np.zeros((len(self.pastplays), 1))
        #labels = np.empty((len(self.pastplays), 1))
        #if winner:
        #    for i in range(len(self.pastplays)):
        #        labels[i] = 0.5 + 0.5*float(i)/len(self.pastplays)
        #else:
        #    for i in range(len(self.pastplays)):
        #        labels[i] = 0.5 - 0.5*float(i)/len(self.pastplays)
        
        #np_labels = np.asarray(self.labels, dtype=np.float32)
        features = np.asarray(self.pastplays, dtype=np.float32)
        if winner:
            np_labels = np.ones((len(self.pastplays), 1))
        self.model.fit(features,np_labels,verbose=0)
        self.pastplays = []
        self.labels = []

    def play(self):
        #update counts if opponent has discarded cards or discards were added back to deck
        diff = len(self.game.discard_pile.cards) - self.discard_len
        if diff > 0: #opponent played cards
            for i in range(diff):
                discarded = self.game.discard_pile.cards[i]
                color_idx = self.colors.index(discarded.color)
                self.color_counts[color_idx] -= 1
                self.value_counts[discarded.value] -= 1
                self.flag_counts[discarded.flag] -= 1
        elif diff < 0: #first play, or deck reshuffled
            self.update_totals()
        self.discard_len = len(self.game.discard_pile.cards)
        
        ##compare opponent hand length to hand at last turn
        len_opp_hand = len(self.game.player2.hand.cards)
        opp = self.game.player2
        if self.game.player2.name == self.name:
            opp = self.game.player1
            len_opp_hand = len(self.game.player1.hand.cards)
        
        if self.discard_or_draw():
            drawn_card = self.draw()
            if type(drawn_card) == int:
                return [1, -1, self.game.wild_color]
            color_idx = self.colors.index(drawn_card.color)
            self.color_counts[color_idx] -= 1
            self.value_counts[drawn_card.value] -= 1
            self.flag_counts[drawn_card.flag] -= 1
            self.opp_hand_len = len_opp_hand
            return [1,drawn_card,self.game.wild_color]
        else:
            possible_discards = self.all_possible_cards()
            i, wild_color, prob = self.select_discard(possible_discards,len_opp_hand,opp)
            discard_card = possible_discards[i]
            self.discard_len += 1
            self.opp_hand_len = len_opp_hand
            return [0,self.discard(discard_card),wild_color]
        
    def select_discard(self,possible_discards,len_opp_hand,opp):
        hand_colors = [0]*5
        hand_values = [0]*11
        hand_flags = [0]*6
        for c in self.hand.cards:
            color_idx = self.colors.index(c.color)
            hand_colors[color_idx] += 1
            hand_values[c.value] += 1
            hand_flags[c.flag] += 1
            
        opp_hand_diff = len_opp_hand - self.opp_hand_len
        
        drawn = 0
        if opp_hand_diff > 0: #opponent had to draw card(s)
            drawn = 1
        
         
        best_idx = 0
        best_val = -100000
        best_wild = None
        best_vector = []
        for i in range(len(possible_discards)):
            d = possible_discards[i]
            compare_to_last = [0]*3
            if d.color == (self.game.recent_played_card.color) or (d.color == self.game.wild_color):
                compare_to_last[0] = 1
            if d.value == self.game.recent_played_card.value:
                compare_to_last[1] = 1
            if d.flag == self.game.recent_played_card.flag:
                compare_to_last[2] = 1
            
            wild_color = None
            if d.flag >= 4:
                wild_color = self.select_wild_color()
                if wild_color == self.game.wild_color:
                    compare_to_last[0] = 1
                    
            num_possible = self.possible_card_percent(self.hand.cards,d,wild_color)-1
            
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
            
            vector = hand_colors2 + hand_values2 + hand_flags2 + compare_to_last + [drawn,num_possible] + color_dist + \
                value_dist + flag_dist + [len_opp_hand] + discard_colors + discard_values + discard_flags
            #vector = hand_colors2 + hand_values2 + hand_flags2 + compare_to_last + [drawn,num_possible,len_opp_hand]
            val = self.model.predict(np.array(vector, dtype=np.float32).reshape(1,len(vector)))
            #print(len(vector))
            #print(val)
            if val > best_val:
                best_idx = i
                best_val = val
                best_wild = wild_color
                best_vector = vector
        if self.update_label:
            #self.labels.append([opp_hand_diff])
            #self.labels[len(self.labels)-1][0] += self.h(-1,opp.hand.cards)
            self.update_label = False
        if (best_val > -100000) and (len(possible_discards) > 1): #only add if player actually had to make decision
            self.pastplays.append(best_vector)
            self.labels.append([-1*self.h(possible_discards[best_idx],self.hand.cards)])
            self.update_label = True
        return best_idx, best_wild, best_val
    
    #updates counts of what cards the player hasn't seen in their hand or discarded  
    def update_totals(self):
        self.color_counts = [0]*5
        self.value_counts = [0]*11
        self.flag_counts = [0]*6
        
        #accumulate counts of cards we haven't seen
        for i in range(len(self.game.deck.cards)):
            color_idx = self.colors.index(self.game.deck.cards[i].color)
            self.color_counts[color_idx] += 1
            self.value_counts[self.game.deck.cards[i].value] += 1
            self.flag_counts[self.game.deck.cards[i].flag] += 1
        opp_player = self.game.player2
        if opp_player.name == self.name:
            opp_player = self.game.player1
        for i in range(len(opp_player.hand.cards)):
            color_idx = self.colors.index(opp_player.hand.cards[i].color)
            self.color_counts[color_idx] += 1
            self.value_counts[opp_player.hand.cards[i].value] += 1
            self.flag_counts[opp_player.hand.cards[i].flag] += 1
    
    def possible_card_percent(self,hand,discard,wild_color):
        count = 0
        for card in hand:
            if (card.flag >= 4):
                count += 1
            if (card.flag >= 1) and (card.flag == discard.flag):
                count += 1
            if (card.value == discard.value) and (card.flag == 0):
                count += 1
            if card.color == discard.color:
                count += 1
            if card.color == wild_color:
                count += 1
        return count
               
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
    
    #use this only for pre-training to get similar to heuristic_v2
    def h(self, possible_card, hand):
        hVal = len(hand) - 1
        newHand = hand[:]
        if type(possible_card) != int:
            newHand.remove(possible_card)
        for c in newHand:
            if c.flag == 0:
                hVal += c.value
            elif c.flag == 1 or c.flag == 2:
                hVal += 10
            elif c.flag == 3:
                hVal += 12
            # elif c.flag == 4:
            #     hVal += 14
            # elif c.flag == 5:
            #     hVal += 16
        return hVal

    def say_uno(self):
        self.game.uno(self)
