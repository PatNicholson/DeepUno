"""
Train the neural network by having it play against itself
"""

import sys
from objects import *
from reinforce_nn import reinforce_nn
from reinforce_nn_fullinfo import reinforce_nn_fi
from control import Control
from heuristic_v1 import Heuristic_v1
from heuristic_v2 import Heuristic_v2

import numpy as np
np.random.seed(1337) # for reproducibility

from keras.layers import Input
from keras.models import Sequential, model_from_json, Model
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Dense, Dropout, Flatten, concatenate
from keras.optimizers import RMSprop, SGD


import random
random.seed()



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

training = False
nlayers = 1

if nlayers == 1: #model based on one layer
    model = Sequential()
    model.add(Dense(20, input_shape=(67,)))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('linear'))
    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    if not training:
        model.load_weights('model_reinforce.h5')
else: #model based on two layers
    model = Sequential()
    model.add(Dense(32, input_shape=(67,)))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('linear'))
    rms = RMSprop()
    model.compile(loss='mse', optimizer=rms)
    if not training:
        model.load_weights('model_reinforce_v2_fullinfo.h5')

def next_player(game):
    if game.turn == game.player1:
        return game.player2
    return game.player1

def score(hand):
    s = 0
    for c in hand:
        if c.flag == 0:
            s += c.value
        elif c.flag >= 1 and c.flag <= 3:
            s += 20
        elif c.flag >= 4:
            s += 50
    return s


#training or testing the model

wins = 0
total = 0
P1_turns = 0
P2_turns = 0
P1_score = 0
P2_score = 0
output = ''
rounds = 500

for i in range(rounds):
    game = UNO_Game(Deck())
    game.player1 = reinforce_nn(game,'P1', model)
    game.player2 = Heuristic_v2(game,'P2')

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
        if training:
            game.player1.train(1)
        wins += 1
        P1_turns += t
        P1_score += score(game.player2.hand.cards)
    else:
        if training:
            game.player1.train(0)
        P2_turns += t
        P2_score += score(game.player1.hand.cards)
    total += 1
    if training and (i%200 == 199):
        print('round',i)
        print(wins/float(total))
        print(P1_turns/float(wins))
        print(P2_turns/float(200-wins))
        output += str(i) + ',' + str(wins/float(total)) + '\n'
        wins = 0
        total = 0
        P1_turns = 0
        P2_turns = 0
        
if not training:
    print(wins/float(total))
    print(P1_turns/float(wins))
    print(P2_turns/float(rounds-wins))
    print(P1_score/float(wins))
    print(P2_score/float(rounds-wins))
else:
    # serialize model to JSON
    model_json = model.to_json()
    with open("model_reinforce_v2.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model_reinforce_v2.h5")
    print("Saved model to disk")

    with open('nn_training_v2.csv','w') as f:
        f.write(output)




