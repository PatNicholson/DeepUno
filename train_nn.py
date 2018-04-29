
from qplayer import Qplayer
from dqn import Dqn_player

def main():
    num_learning_rounds = 20000
    game = UNO_Game(num_learning_rounds, qplayer()) # need to fix this
    number_of_test_rounds = 1000
    for k in range(0,num_learning_rounds + number_of_test_rounds):
        game.run()

    df = game.p.get_optimal_strategy()
    print(df)
    df.to_csv('optimal_policy.csv')