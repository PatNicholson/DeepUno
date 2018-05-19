"""
Heuristic AI. Plays randomly.
"""

from objects import *
import random

class Heuristic_dt(Player):
    def __init__(self, game, name, num_trials = 10, hand_size = 7):
        Player.__init__(self,game,name, hand_size)
        self.len_opp_hand = 7
        self.num_trials = num_trials
        self.opp_color_upper = [7]*5 #keep track of what colors opp can and cannot have
        self.opp_value_upper = [7]*11 #keep track of what values opp can and cannot have
        self.opp_value_upper[0] = 4
        self.opp_flag_upper = [7]*6 #keep track of what special cards opp can and cannot have
        self.opp_flag_upper[4] = 4
        self.opp_flag_upper[5] = 4
        self.colors = ["red", "blue", "green", "yellow", None]
        self.last_discard_len = 1

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

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0

    def play(self):
        #see how discard and opp hands have changed
        opp_player = self.game.player2
        if opp_player.name == self.name:
            opp_player = self.game.player1
        diff_discard = len(self.game.discard_pile.cards) - self.last_discard_len
        diff_opp = len(opp_player.hand.cards) - self.len_opp_hand
        
        if (diff_opp > diff_discard) and (diff_discard >= 0):
            self.update_bounds(opp_player)
        
        self.last_discard_len = len(self.game.discard_pile.cards)
        self.len_opp_hand = len(opp_player.hand.cards)
        
        if self.discard_or_draw():
            return [1,self.draw(),None]
        else:
            wild_color = None
            possible_discards = self.all_possible_cards()
            
            discard_card = self.select_discard(possible_discards,opp_player)
            if discard_card.flag >= 4:
                wild_color = self.select_wild_color()
                if discard_card.flag == 5:
                    self.len_opp_hand += 4
            elif discard_card.flag == 3:
                self.len_opp_hand += 2
            self.last_discard_len += 1
            return [0,self.discard(discard_card),wild_color]
        
    def update_bounds(self,opp_player):
        #update colors
        color_idx = self.colors.index(self.game.recent_played_card.color)
        self.opp_color_upper[color_idx] = 0
        for i in range(5):
            self.opp_color_upper[i] = min(self.opp_color_upper[i]+1,len(opp_player.hand.cards))
        #update values
        if self.game.recent_played_card.value != 10:
            self.opp_value_upper[self.game.recent_played_card.value] = 0
        for i in range(1,10):
            self.opp_value_upper[i] = min(self.opp_value_upper[i]+1,len(opp_player.hand.cards),8)
        self.opp_value_upper[0] = min(self.opp_value_upper[0]+1,len(opp_player.hand.cards),4)
        #update flags
        if self.game.recent_played_card.flag != 0:
            self.opp_flag_upper[self.game.recent_played_card.flag] = 0
        for i in range(1,4):
            self.opp_flag_upper[i] = min(self.opp_flag_upper[i]+1,len(opp_player.hand.cards),8)
        self.opp_flag_upper[4] = min(self.opp_flag_upper[4]+1,len(opp_player.hand.cards),4)
        self.opp_flag_upper[5] = min(self.opp_flag_upper[5]+1,len(opp_player.hand.cards),4)
        
    def select_discard(self,possible_discards,opp_player):
        best_score = 100000
        best_idx = 0
        for i in range(len(possible_discards)):
            card = possible_discards[i]
            if self.len_opp_hand <= 1 and (card.flag in [1,2,3,5]): #near end game, should always use special cards
                return card
            
            wild_color = None
            if card.flag >= 4:
                if len(self.hand.cards) > 2:
                    continue
                wild_color = self.select_wild_color()
            num_poss = self.possible_card_percent(self.hand.cards,card,wild_color)
            if ((card.flag == 1) or (card.flag == 2)) and (num_poss > 0): #if you can skip and keep playing, do so
                return card
            
            if num_poss > 0:
                score = self.opp_value_upper[card.value] + self.opp_color_upper[self.colors.index(card.color)]
                if card.value == 10:
                    score = self.opp_flag_upper[card.flag] + self.opp_color_upper[self.colors.index(card.color)]
                if score < best_score:
                    best_score = score
                    best_idx = i
        return possible_discards[best_idx]

    
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
    
    def say_uno(self):
        self.game.uno(self)