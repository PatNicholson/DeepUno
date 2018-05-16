"""
Control AI. Plays randomly.
"""

from objects import *
import random
from minmax import *

random.seed()

class TreeSearchPlayer(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)
        self.colors = ["red", "blue", "green", "yellow"]
        self.deck_dict = [] #maps and index to a unique card type
        self.card_to_idx = {} #maps a unique card type to an index
        self.counts = [] #tracks the number of each card type not yet seen
        self.discard_len = 1000000 #ensure totals are updated at first play

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0

    def play(self):
        #update counts if opponent has discarded cards or discards were added back to deck
        diff = len(self.game.discard_pile.cards) - self.discard_len
        if diff > 0: #opponent played cards
            for i in range(diff):
                discarded = self.game.discard_pile.cards[i]
                self.counts[self.card_to_idx[str(discarded)]] -= 1
        elif diff < 0: #first play, or deck reshuffled
            self.update_totals()
        self.discard_len = len(self.game.discard_pile.cards)
        
        
        if self.discard_or_draw():
            drawn_card = self.draw()
            self.counts[self.card_to_idx[str(drawn_card)]] -= 1
            return [1,drawn_card,self.game.wild_color]
        else:
            possible_discards = self.all_possible_cards()
            i, wild_color = self.select_discard(possible_discards)
            discard_card = possible_discards[i]
            self.discard_len += 1
            return [0,self.discard(discard_card),wild_color]
        
    def select_discard(self,possible_discards):
        hand = [0]*len(self.deck_dict)
        for c in self.hand.cards:
            hand[self.card_to_idx[str(c)]] += 1
        len_opp_hand = len(self.game.player2.hand.cards)
        if self.game.player2.name == self.name:
            len_opp_hand = len(self.game.player1.hand.cards)
         
        best_idx = 0
        best_val = 0
        best_wild = None
        for i in range(len(possible_discards)):
            d = possible_discards[i]
            wild_color = None
            if d.flag >= 4:
                wild_color = self.select_wild_color()
            discard = [0]*len(self.deck_dict)
            discard[self.card_to_idx[str(d)]] = 1
            hand_copy = hand[:]
            hand_copy[self.card_to_idx[str(d)]] -= 1
            vector = hand_copy + self.counts + [len_opp_hand] + discard
            val = min_max(self.deck_dict, len(self.deck_dict), vector, 5, wild_color, 5)
            if val > best_val:
                best_idx = i
                best_val = val
                best_wild = wild_color
        return best_idx, best_wild
    
    #updates counts of what cards the player hasn't seen in their hand or discarded  
    def update_totals(self):
        self.deck_dict = [] #maps and index to a unique card type
        self.card_to_idx = {} #maps a unique card type to an index
        self.counts = [] #tracks the number of each card type not yet seen
        
        #accumulate counts of cards we haven't seen
        idx = 0
        for i in range(len(self.game.deck.cards)):
            if not self.game.deck.cards[i] in self.deck_dict:
                self.deck_dict.append(self.game.deck.cards[i])
                self.card_to_idx[str(self.deck_dict[idx])] = idx
                self.counts.append(1)
                idx += 1
            else:
                self.counts[self.card_to_idx[str(self.game.deck.cards[i])]] += 1
        opp_player = self.game.player2
        if opp_player.name == self.name:
            opp_player = self.game.player1
        for i in range(len(opp_player.hand.cards)):
            if not opp_player.hand.cards[i] in self.deck_dict:
                self.deck_dict.append(opp_player.hand.cards[i])
                self.card_to_idx[str(self.deck_dict[idx])] = idx
                self.counts.append(1)
                idx += 1
            else:
                self.counts[self.card_to_idx[str(opp_player.hand.cards[i])]] += 1
                
        #add mappings for cards in hand, in case they weren't
        #seen in deck or opponent's hand
        for i in range(len(self.hand.cards)):
            if not self.hand.cards[i] in self.deck_dict:
                self.deck_dict.append(self.hand.cards[i])
                self.card_to_idx[str(self.deck_dict[idx])] = idx
                self.counts.append(0)
                idx += 1
                
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
