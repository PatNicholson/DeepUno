"""
This file defines all the major classes that will be used:

Card: represents an UNO card in the deck
Deck: represents a list of cards
Player: treated as an abstract or super class that each AI player will implement
Game: represents the state of a single game (the one that is currently being
      played)

Weights on cards for scoring:
  Card : weight for score
  0 : 0
  1 : 1
  2 : 2
  3 : 3
  4 : 4
  5 : 5
  6 : 6
  7 : 7
  8 : 8
  9 : 9
  skip/reverse : 10
  draw 2 : 12
  wild : 14
  wild draw 4 : 16

"""

import random

random.seed()

""" Represents current state of the game that is being played. """
class UNO_Game:
    def __init__(self, new_deck, player1 = None, player2 = None):
        self.player1 = player1
        self.player2 = player2
        self.turn = player1

        self.deck = new_deck

        self.recent_played_card = self.deck.cards.pop(0)
        print('recently played card')
        print(self.recent_played_card)
        i = 1
        while self.recent_played_card.flag >= 4:
            self.deck.add(self.recent_played_card)
            self.recent_played_card = self.deck.cards.pop(i)
            i += 1
            print('recently played card')
            print(self.recent_played_card)
        self.discard_pile = Deck(0)
        self.discard_pile.add(self.recent_played_card)

        self.wild_color = None

    def uno(self,player):
        if player.hand.size_of_deck == 1:
            return True
        return False

    def game_over(self,player):
        if len(player.hand.cards) == 0:
            return True
        return False


""" Represents a player """
class Player:
    def __init__(self, game, name):
        self.name = name
        self.game = game
        self.hand = Deck(0)
        for i in range(7):
            self.draw()

    def draw(self):
        card_drawn = self.game.deck.draw()
        self.hand.add(card_drawn)
        if self.game.deck.empty():
            self.game.recent_played_card = self.game.discard_pile.draw()
            self.game.discard_pile.shuffle()
            self.game.deck = self.game.discard_pile
            self.game.discard_pile = Deck(0)
            self.game.discard_pile.add(self.game.recent_played_card)
        return card_drawn

    def discard(self, card):
        self.hand.discard(card)
        self.game.recent_played_card = card
        self.game.discard_pile.add(card)
        return card

    """ 0 if discard, 1 if draw"""
    def discard_or_draw(self):
        raise NotImplementedError("discard_or_draw not implemented")

    """ returns 3 values:
    - 0 if discard, 1 if draw
    - the discarded or drawn card
    - the chosen color if a wildcard is played, 'None' otherwise
    """
    def play(self):
        raise NotImplementedError("play not implemented")

    def possible_card(self):
        for card in self.hand.cards:
            if (card.flag >= 4):
                return True
            if (card.flag >= 1) and (card.flag == self.game.recent_played_card.flag):
                return True
            if (card.value == self.game.recent_played_card.value) and (card.flag == 0):
                return True
            if card.color == self.game.recent_played_card.color:
                return True
            if card.color == self.game.wild_color:
                return True
        return False

    def all_possible_cards(self):
        all_possible_cards = Deck(0)
        for card in self.hand.cards:
            if (card.flag >= 4):
                all_possible_cards.add(card)
            elif (card.flag >= 1) and (card.flag == self.game.recent_played_card.flag):
                all_possible_cards.add(card)
            elif (card.value == self.game.recent_played_card.value) and (card.flag == 0):
                all_possible_cards.add(card)
            elif card.color == self.game.recent_played_card.color:
                all_possible_cards.add(card)
            elif card.color == self.game.wild_color:
                all_possible_cards.add(card)
        return all_possible_cards.cards


""" Represents an UNO card.
value: numerical value of a regular (non-special or non-wild) card
       between 0 and 9 for regular cards; 10 for non-regular
color: color of a non-wild card
       red, blue, green, yellow, or None (if wild)
flag: indicates if a card is special or wild
      0: regular
      1: reverse
      2: skip
      3: draw 2
      4: wild
      5: wild draw 4
"""
class Card:
    def __init__(self, value, color, flag):
        self.value = value
        self.color = color
        self.flag = flag

"""Represents a list of cards. The first card in the list represents
the top of the deck, or the card that can be drawn"""
class Deck:
    def __init__(self, deck_size = 108):
        self.cards = []
        colors = ["red", "blue", "green", "yellow"]
        nums = range(1,10)
        if deck_size == 108:
            for color in colors:
                self.cards.append(Card(0,color,0))
                for n in nums:
                    self.cards.append((Card(n,color,0)))
                    self.cards.append((Card(n,color,0)))
                self.cards.append(Card(10,color,1))
                self.cards.append(Card(10,color,1))
                self.cards.append(Card(10,color,2))
                self.cards.append(Card(10,color,2))
                self.cards.append(Card(10,color,3))
                self.cards.append(Card(10,color,3))
            for i in range(4):
                self.cards.append(Card(10,None,4))
                self.cards.append(Card(10,None,5))
            self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def size_of_deck(self):
        return len(self.cards)

    def draw(self):
        return self.cards.pop(0)

    def add(self,card):
        self.cards = [card] + self.cards

    def empty(self):
        if len(self.cards) == 0:
            return True
        return False

    def discard(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            for c in self.cards:
                if (c.value==card.value) and (c.flag==card.flag) and (c.color==card.color):
                    self.cards.remove(c)
                    break


