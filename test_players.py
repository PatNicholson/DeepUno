import csv

player1 = "Control"
player2 = "Heuristic_v2"

file_name = player1+"_"+player2+".csv"

f = open(file_name,"a")

for i in range(1):
    import ai_unogame as playedGame
    winner = playedGame.winner
    if winner == 'P1':
        winner = player1
    elif winner == 'P2':
        winner = player2
    turns = playedGame.t
    result = player1+","+player2+","+winner+","+str(turns)+"\n"
    f.write(result)

f.close()

