"""
Control AI. Plays randomly.
"""

from objects import *
import random

class Control(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0

    def play(self):
        if discard_or_draw:
            return self.draw()
        else:
            possible_discards = self.all_possible_cards()
            i = random.randint(0,len(possible_discards))
            discard_card = possible_discards[i]
            return self.discard(discard_card)
