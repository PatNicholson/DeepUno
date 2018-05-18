"""
Heuristic AI. Plays randomly.
"""

from objects import *
import random

class Combination(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)
        self.num_opponent_cards = 7 #number of cards in opponent's hand
        self.opponent_drew_color = [] #list of colors (strings)
        self.opponent_drew_number = [] #list of values (ints)
        self.recent_play = None #card that was most recently played by this player
        self.recent_play_wild = None #color if wild was most recently played, None otherwise

    """Computes the value h to the opponent's hand if the player discards
    possible_card on this turn"""
    def opp_h(self, possible_card):
        hVal = 0

        for c in self.opponent_drew_color:
            if possible_card.color == c:
                hVal += 10

        for n in self.opponent_drew_number:
            if possible_card.value == n:
                hVal += n

        return hVal

    """Computes the value h of the player's hand if the player discards
    possible_card on this turn"""
    def self_h(self, possible_card):
        hVal = len(self.hand.cards) - 1
        newHand = self.hand.cards[:]
        newHand.remove(possible_card)
        for c in newHand:
            if c.flag == 0:
                hVal += c.value
            elif c.flag == 1 or c.flag == 2:
                hVal += 10
            elif c.flag == 3:
                hVal += 12
        return hVal

    def opp_select_wild_color(self):
        yellow = 0
        red = 0
        blue = 0
        green = 0
        for c in self.opponent_drew_color:
            if c == "yellow":
                yellow += 1
            elif c == "red":
                red += 1
            elif c == "blue":
                blue += 1
            elif c == "green":
                green += 1
        best_option = (max((yellow,"yellow"),(red,"red"),(blue,"blue"),
            (green,"green")))[1]
        return best_option

    def self_select_wild_color(self):
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

    def check_opponent(self):
        if self.game.deck.cards[0] == self.recent_play:
            self.num_opponent_cards += 1
            if self.recent_play.flag < 4:
                self.opponent_drew_color.append(self.recent_play.color)
            if self.recent_play.flag == 0:
                self.opponent_drew_number.append(self.recent_play.value)
            if self.recent_play.flag >= 4:
                self.opponent_drew_color.append(self.recent_play_wild)

        else:
            self.num_opponent_cards -= 1
            for c in self.opponent_drew_color:
                if self.game.deck.cards[0].color == c:
                    self.opponent_drew_color.remove(c)
            for n in self.opponent_drew_number:
                if self.game.deck.cards[0].value == n:
                    self.opponent_drew_number.remove(n)

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0

    def play(self):
        self.check_opponent()

        if self.discard_or_draw():
            return [1,self.draw(),None]

        else:
            wild_color = None
            possible_discards = self.all_possible_cards()

            if self.num_opponent_cards < 3:

                discard_card = possible_discards[0]
                score = self.opp_h(discard_card)

                for i in range(1,len(possible_discards)):
                    newScore = self.opp_h(possible_discards[i])
                    if newScore > score:
                        discard_card = possible_discards[i]

                if discard_card.flag >= 4:
                    wild_color = self.opp_select_wild_color()

            else:

                discard_card = possible_discards[0]
                score = self.self_h(discard_card)

                for i in range(1,len(possible_discards)):
                    newScore = self.self_h(possible_discards[i])
                    if newScore < score:
                        discard_card = possible_discards[i]

                if discard_card.flag >= 4:
                    wild_color = self.self_select_wild_color()

            if discard_card.flag == 3:
                self.num_opponent_cards += 2

            if discard_card.flag == 5:
                self.num_opponent_cards += 4

            self.recent_play = discard_card
            self.recent_play_wild = wild_color

            return [0,self.discard(discard_card),wild_color]

    def say_uno(self):
        self.game.uno(self)