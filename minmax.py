from objects import *
import numpy as np
import copy

#vector contain the following:
# - for the first 'card_type' elements, 1 if
#   that card is in player's hand, 0 otherwise
# - for the second 'card_type' elments, the number
#   of that card that have not been seen (i.e. not seen
#   in your hand or by being played by opponent)
# - for last element, the number of cards in opponent's hand
def min_max(deck_dict, card_types, vector, trials, wild_color, maxdepth):
    hand = []
    for i in range(card_types): #fill the player's hand
        if vector[i] >= 1:
            for j in range(vector[i]):
                hand.append(deck_dict[i])
    totals_init = vector[card_types:(2*card_types)]
    discard_idx = vector[(2*card_types+1):(3*card_types+1)].index(1)
    discard_top = deck_dict[discard_idx] #get card on top of discard pile
    p = [x/float(sum(totals_init)) for x in totals_init]
    minmax_total = 0
    for i in range(trials):
        print('trial',str(i))
        totals = totals_init[:]
        p2 = p
        opp_card_indices = np.random.choice(card_types, vector[2*card_types], p=p2)
        opp_hand = []
        for i in range(len(opp_card_indices)): #fill opponent hand
            opp_hand.append(deck_dict[opp_card_indices[i]])
            totals[opp_card_indices[i]] -= 1
        
        deck = Deck(0)
        for i in range(len(totals)): #fill the deck of cards remaining
            for j in range(totals[i]):
                deck.add(deck_dict[i])
        deck.shuffle()
        minmax_val_t = min_max_helper(hand, opp_hand, discard_top, deck, 0, 0, wild_color, 1, maxdepth)
        minmax_total += minmax_val_t
    
    return minmax_total/float(trials)

def min_max_helper(hand, opp_hand, discard_top, deck, turn, prune, wild_color, depth, maxdepth):
    if len(opp_hand) == 0:
        return 0
    elif len(hand) == 0:
        return 1
    elif (depth > maxdepth) or (len(deck.cards) <= 4):
        return len(opp_hand)/float(len(opp_hand)+len(hand)) #return opp hand len over sum of both hands as heuristic
    elif turn == 1: #player's turn, aim to maximize value
        poss_card_idx = all_possible_cards(hand, discard_top, wild_color)
        if len(poss_card_idx) == 0: #have to draw a card
            deck2 = copy.deepcopy(deck)
            hand2 = hand[:]
            hand2.append(deck2.cards.pop(0))
            return min_max_helper(hand2, opp_hand, discard_top, deck2, 0, 0, wild_color, depth+1, maxdepth)
        else: #recurse down various choice paths
            max_val = 0
            for i in range(len(poss_card_idx)):
                hand2 = hand[:]
                discard_top2 = hand2.pop(poss_card_idx[i])
                if discard_top2.flag >= 4: #iterate through all possible wild color choices
                    deck2 = copy.deepcopy(deck)
                    opp_hand2 = opp_hand[:]
                    if discard_top2.flag == 5: #opponent draws 4 cards
                        for d in range(4):
                            opp_hand2.append(deck2.cards.pop(0))
                    colors = ["red", "blue", "green", "yellow"]
                    for j in range(4):
                        tmp_val = min_max_helper(hand2, opp_hand2, discard_top2, deck2, 0, max_val, colors[j], depth+1, maxdepth)
                        max_val = max(max_val,tmp_val)
                        if max_val >= prune:
                            return prune
                elif (discard_top2.flag == 1) or (discard_top2.flag == 2): #skip other player
                    tmp_val = min_max_helper(hand2, opp_hand, discard_top2, deck, 1, prune, None, depth+1, maxdepth)
                elif discard_top2.flag == 3: #opponent draws 2 cards
                    deck2 = copy.deepcopy(deck)
                    opp_hand2 = opp_hand[:]
                    opp_hand2.append(deck2.cards.pop(0))
                    opp_hand2.append(deck2.cards.pop(0))
                    tmp_val = min_max_helper(hand2, opp_hand2, discard_top2, deck2, 0, max_val, None, depth+1, maxdepth)
                else:
                    tmp_val = min_max_helper(hand2, opp_hand, discard_top2, deck, 0, max_val, None, depth+1, maxdepth)
                max_val = max(max_val,tmp_val)
                if max_val >= prune:
                    return prune
            return max_val
        
    else: #opponent's turn, aim to minimize value
        poss_card_idx = all_possible_cards(opp_hand, discard_top, wild_color)
        if len(poss_card_idx) == 0: #have to draw a card
            deck2 = copy.deepcopy(deck)
            opp_hand2 = opp_hand[:]
            opp_hand2.append(deck2.cards.pop(0))
            return min_max_helper(hand, opp_hand2, discard_top, deck2, 1, 1, wild_color, depth+1, maxdepth)
        else: #recurse down various choice paths
            min_val = 1
            for i in range(len(poss_card_idx)):
                opp_hand2 = opp_hand[:]
                discard_top2 = opp_hand2.pop(poss_card_idx[i])
                if discard_top2.flag >= 4: #iterate through all possible wild color choices
                    deck2 = copy.deepcopy(deck)
                    hand2 = hand[:]
                    if discard_top2.flag == 5: #player draws 4 cards
                        for d in range(4):
                            hand2.append(deck2.cards.pop(0))
                    colors = ["red", "blue", "green", "yellow"]
                    for j in range(4):
                        tmp_val = min_max_helper(hand2, opp_hand2, discard_top2, deck2, 1, min_val, colors[j], depth+1, maxdepth)
                        min_val = min(min_val,tmp_val)
                        if min_val <= prune:
                            return prune
                elif (discard_top2.flag == 1) or (discard_top2.flag == 2): #skip other player
                    tmp_val = min_max_helper(hand, opp_hand2, discard_top2, deck, 0, prune, None, depth+1, maxdepth)
                elif discard_top2.flag == 3: #opponent draws 2 cards
                    deck2 = copy.deepcopy(deck)
                    hand2 = hand[:]
                    hand2.append(deck2.cards.pop(0))
                    hand2.append(deck2.cards.pop(0))
                    tmp_val = min_max_helper(hand2, opp_hand2, discard_top2, deck2, 1, min_val, None, depth+1, maxdepth)
                else:
                    tmp_val = min_max_helper(hand, opp_hand2, discard_top2, deck, 1, min_val, None, depth+1, maxdepth)
                min_val = min(min_val,tmp_val)
                if min_val <= prune:
                    return prune
            return min_val
        
def all_possible_cards(cards, last_played, wild_color):
    all_possible_cards = []
    for i in range(len(cards)):
        card = cards[i]
        if (card.flag >= 4):
            all_possible_cards.append(i)
        elif (card.flag >= 1) and (card.flag == last_played.flag):
            all_possible_cards.append(i)
        elif (card.value == last_played.value) and (card.flag == 0):
            all_possible_cards.append(i)
        elif card.color == last_played.color:
            all_possible_cards.append(i)
        elif card.color == wild_color:
            all_possible_cards.append(i)
    return all_possible_cards
    

