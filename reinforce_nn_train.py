"""
Train the neural network by having it play against itself
"""

import sys
from objects import *
from reinforce_nn import reinforce_nn
from control import Control

from keras.layers import Input
from keras.models import Sequential, model_from_json, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Dense, Dropout, Flatten, concatenate
from keras.optimizers import RMSprop, SGD
import numpy as np



# model with multiple inputs 
# WIP
"""
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

hand = Input(shape=(4,), name = "hand_cards")
hand_size = Input(shape=(1,), name = "hand_size")
deck_size = Input(shape=(1,), name = "deck_size")
opponent_hand = Input(shape=(1,), name = "opponent_hand")
top_discard = Input(shape=(4,), name = "top_discard")


hidden11 = Dense(108, activation='relu', input_dim=(4,))(hand)
dropout11 = Dropout(0.5)(hidden11)
hidden12 = Dense(108, activation='relu')(hand)
dropout11 = Dropout(0.5)(hidden12)
#flat1 = Flatten()(dropout11)

hand_size_input = Dense(1, activation='relu', input_dim=(1,))(opponent_hand)

# merge input models
merge = concatenate([dropout11, hand_size_input])

# interpretation model
hidden_all1 = Dense(108, activation='relu')(merge)
hidden_all2 = Dense(108, activation='relu')(hidden_all1)
output = Dense(1, activation='sigmoid')(hidden_all2)
model = Model(inputs=[hand, hand_size], outputs=output)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
"""

"""
#original model
model = Sequential()
model.add(Dense(1, init='lecun_uniform', input_shape=(4,)))
model.add(Activation('relu'))
model.add(Dense(108, init='lecun_uniform'))
model.add(Activation('relu'))
model.add(Dense(1, init='lecun_uniform'))
model.add(Activation('linear'))
rms = RMSprop()
model.compile(loss='mse', optimizer=rms)
"""

#model based on one layer
model = Sequential()
model.add(Dense(20, input_shape=(67,)))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('linear'))
rms = RMSprop()
model.compile(loss='mse', optimizer=rms)


def next_player(game):
    if game.turn == game.player1:
        return game.player2
    return game.player1

#training the model
wins = 0
total = 0
for i in range(10000):
    game = UNO_Game(Deck())
    #default is two control players
    game.player1 = reinforce_nn(game,'P1', model)
    game.player2 = Control(game,'P2')

    game.turn = game.player1 #P1 gets first turn

    #game loop
    winner = None
    t = 0
    while (not game.game_over(game.turn)) and (t < 100000):
        t += 1
        [play_type,card,game.wild_color] = game.turn.play()

        if game.game_over(game.turn):
            winner = game.turn.name
            model = game.player1.model
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
    
    if winner == 'P1':
        game.player1.train(1)
        wins += 1
    else:
        game.player1.train(0)
    total += 1
    print(wins/float(total))

# serialize model to JSON
#model_json = model.to_json()
#with open("model.json", "w") as json_file:
#    json_file.write(model_json)
# serialize weights to HDF5
#model.save_weights("model.h5")
#print("Saved model to disk")




