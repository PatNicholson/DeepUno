"""
Train the neural network by having it play against itself
"""

import sys
from objects import *
from nn import simple_nn

from keras.models import Sequential, model_from_json
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

#training the model
for i in range(1000):
    game = UNO_Game(Deck())
    #default is two control players
    game.player1 = simple_nn(game,'P1', model, training = True)
    game.player2 = simple_nn(game,'P2', model, training = True)

    game.turn = game.player1 #P1 gets first turn

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
            game.turn = next_player(game)

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")




