"""
Control AI. Plays randomly.
"""

from objects import *
import random

class Control(Player):
    def __init__(self, game, name):
        Player.__init__(self,game,name)
        self.colors = ["red", "blue", "green", "yellow"]

    def discard_or_draw(self):
        if not self.possible_card():
            return 1
        return 0

    def play(self):
        if self.discard_or_draw():
            return [1,self.draw(),self.game.wild_color]
        else:
            wild_color = None
            possible_discards = self.all_possible_cards()
            i = random.randint(0,len(possible_discards)-1)
            discard_card = possible_discards[i]
            if discard_card.flag >= 4: #if wild, randomly select new color
                i = random.randint(0,3)
                wild_color = self.colors[i]
            return [0,self.discard(discard_card),wild_color]

    def say_uno(self):
        self.game.uno(self)
