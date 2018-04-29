"""
Heuristic AI. Plays randomly.
"""

from objects import *
import random

random.seed()

class Heuristic_v1(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)

    """Computes the value h of the player's hand if the player discards
    possible_card on this turn"""
    def h(self, possible_card):


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

            if discard_card.flag >= 4: #if wild, randomly select new color
                i = random.randint(0,3)
                wild_color = self.colors[i]
            return [0,self.discard(discard_card),wild_color]

    def say_uno(self):
        self.game.uno(self)