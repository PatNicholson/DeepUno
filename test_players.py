import csv
import importlib
import ai_unogame

player1 = "Heuristic_v1"
player2 = "Combination"

file_name = player1+"_"+player2+".csv"

f = open(file_name,"a")

p1_wins = 0
p2_wins = 0
p1_score = 0
p2_score = 0
p1_percent = 0
p1_turns = 0
p2_turns = 0

num_games = 5000

for i in range(num_games):
    importlib.reload(ai_unogame)
    winner = ai_unogame.winner
    turns = ai_unogame.t
    score = ai_unogame.score

    if winner == "P1":
        winner = player1
        p1_wins += 1
        p1_score += score
        p1_turns += turns

    elif winner == "P2":
        winner = player2
        p2_wins += 1
        p2_score += score
        p2_turns += turns

    result = player1+","+player2+","+winner+","+str(turns)+","+str(score)+"\n"
    f.write(result)

avg_p1_score = p1_score/p1_wins
avg_p2_score = p2_score/p2_wins
p1_percent = p1_wins/num_games * 100
avg_p1_turns = p1_turns/p1_wins
avg_p2_turns = p2_turns/p2_wins

final_result = str(num_games)+","+str(p1_wins)+","+str(p2_wins)+","+str(avg_p1_score)+","+str(avg_p2_score)+","+str(p1_percent)+","+str(avg_p1_turns)+","+str(avg_p2_turns)
f.write(final_result)

f.close()

