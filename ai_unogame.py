import sys
from objects import *
from control import Control

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

game = UNO_Game(Deck())
#default is two control players
game.player1 = Control(game,'P1')
game.player2 = Control(game,'P2')
#options for different kinds of AIs to use
if len(sys.argv) > 1:
    if sys.argv[1] == 'bestfirst':
        print('cannot set player 1 to bestfirst, ai not yet implemented')
if len(sys.argv) > 2:
    if sys.argv[2] == 'bestfirst':
        print('cannot set player 1 to bestfirst, ai not yet implemented')

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
