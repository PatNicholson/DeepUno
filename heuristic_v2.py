"""
Heuristic AI. Plays randomly.
"""

from objects import *
import random

class Heuristic_v2(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)

    """Computes the value h of the player's hand if the player discards
    possible_card on this turn"""
    def h(self, possible_card):
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
            # elif c.flag == 4:
            #     hVal += 14
            # elif c.flag == 5:
            #     hVal += 16
        return hVal

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
        if self.discard_or_draw():
            return [1,self.draw(),None]
        else:
            wild_color = None
            possible_discards = self.all_possible_cards()

            discard_card = possible_discards[0]
            score = self.h(discard_card)

            for i in range(1,len(possible_discards)):
                newScore = self.h(possible_discards[i])
                if newScore < score:
                    discard_card = possible_discards[i]

            if discard_card.flag >= 4:
                wild_color = self.select_wild_color()
            return [0,self.discard(discard_card),wild_color]

    def say_uno(self):
        self.game.uno(self)