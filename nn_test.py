"""
Test the neural network against other players
"""
# using the trained nn model to play uno
# make sure to run nn_train.py first

import sys
from objects import *
from control import Control
from nn import simple_nn
from heuristic_v1 import Heuristic_v1
from heuristic_v2 import Heuristic_v2

from keras.optimizers import RMSprop
from keras.models import model_from_json
import numpy as np


def next_player(game):
    if game.turn == game.player1:
        return game.player2
    return game.player1

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(loss='mse', optimizer=RMSprop())

score = 0
for i in range(100):
	game = UNO_Game(Deck())
	#default is two control players
	game.player1 = Heuristic_v2(game,'P1')
	game.player2 = simple_nn(game,'P2', model, training = True)

	game.turn = game.player1 #P1 gets first turn

	t = 0
	while (not game.game_over(game.turn)) and (t < 100000):
		t += 1
		[play_type,card,game.wild_color] = game.turn.play()

		if game.game_over(game.turn):
			if game.turn.name == 'P2':
				score +=1
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
print(score)
