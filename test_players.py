import csv

player1 = "Control1"
player2 = "Control2"

file_name = player1+"_"+player2+".csv"

f = open(file_name,"a")

for i in range(1)
    import ai_unogame as playedGame
    winner = playedGame.winner
    turns = playedGame.t
    result = player1+","+player2+","+winner+","+turns+"\n"
    f.write(result)

f.close()

