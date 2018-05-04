import sys
from objects import *
from control import Control
from nn import simple_nn

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import RMSprop
import numpy as np

model = Sequential()
model.add(Dense(108, init='lecun_uniform', input_shape=(1,)))
model.add(Activation('relu'))
model.add(Dense(108 * 2, init='lecun_uniform'))
model.add(Activation('relu'))
model.add(Dense(1, init='lecun_uniform'))
model.add(Activation('linear'))
rms = RMSprop()
model.compile(loss='mse', optimizer=rms)


def next_player(game):
    if game.turn == game.player1:
        return game.player2
    return game.player1

def name_from_card(card):
    name = ''
    if card.color == None:
        name += 'black_'
    else:
        name += card.color+'_'

    if card.flag == 0:
        return card.color+'_'+str(card.value)
    elif card.flag == 1:
        return card.color+'_'+'reverse'
    elif card.flag == 2:
        return card.color+'_'+'skip'
    elif card.flag == 3:
        return card.color+'_'+'+2'
    elif card.flag == 4:
        return 'black_wildcard'
    elif card.flag == 5:
        return 'black_+4'

for i in range(100):
    game = UNO_Game(Deck())
    #default is two control players
    game.player1 = simple_nn(game,'P1', model, training = True)
    game.player2 = simple_nn(game,'P2', model, training = True)
    #options for different kinds of AIs to use
    game.turn = game.player1 #P1 gets first turn

    print('size of',game.player1.name,'hand is',str(len(game.player1.hand.cards)))
    print('size of',game.player2.name,'hand is',str(len(game.player2.hand.cards)))
    print('size of discard pile is',str(len(game.discard_pile.cards)))
    print('size of deck is',str(len(game.deck.cards)))
    print('------------------------\n')

    #game loop
    winner = None
    t = 0
    while (not game.game_over(game.turn)) and (t < 100000):
        t += 1
        [play_type,card,game.wild_color] = game.turn.play()

        if game.game_over(game.turn):
            winner = game.turn.name
            model = game.turn.model
            break

        if play_type == 0: #process effects of played card
            print(game.turn.name,'played card',name_from_card(card))
            if (card.flag == 0) or (card.flag == 4):
                game.turn = next_player(game)
            elif card.flag == 3:
                next_player(game).draw()
                next_player(game).draw()
                game.turn = next_player(game)
            elif card.flag == 5:
                for x in range(4):
                    next_player(game).draw()
                game.turn = next_player(game)
        else:
            print(game.turn.name,'drew a card')
            game.turn = next_player(game)
        print('size of',game.player1.name,'hand is',str(len(game.player1.hand.cards)))
        print('size of',game.player2.name,'hand is',str(len(game.player2.hand.cards)))
        print('size of discard pile is',str(len(game.discard_pile.cards)))
        print('size of deck is',str(len(game.deck.cards)))
        print()
    print(winner,'wins the game')





