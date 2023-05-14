import numpy as np

import policies
import envUtils as utils
import monteCarlo as mc
import sarsa
import qLearning as ql

tableInactiveAce = utils.createStateActionValue()
tableActiveAce = utils.createStateActionValue()

k = 0

def episode(tableActiveAce, tableInactiveAce):
    global k 
    k += 1
    utils.ace = False
    visitedSAV = list()

    # creating the deck
    deck = utils.createDeck()

    # assigning cards to player and dealer
    playerHand = [deck.pop(), deck.pop()]
    dealerHand = [deck.pop(), deck.pop()]
    
    policies.playerPolicy(deck, playerHand) # the player policy
    policies.dealerPolicy(deck, dealerHand) # the dealer follows his policy
   
    # # ----------MonteCarlo---------
    # epsilon = np.exp(-k/10000)
    # mc.monteCarlo(deck, tableActiveAce, tableInactiveAce, visitedSAV, playerHand, dealerHand, False, epsilon)
    # # -----------------------------

    # # ------------SARSA-----------
    # epsilon = np.exp(-k/1000)
    # sarsa.sarsa(deck, tableActiveAce, tableInactiveAce, playerHand, dealerHand, epsilon)
    # # ----------------------------

    # ---------Q-Learning---------
    epsilon = np.exp(-k/10000)
    ql.qLearning(deck, tableActiveAce, tableInactiveAce, playerHand, dealerHand, epsilon)
    # ----------------------------
    
    return utils.reward(playerHand, dealerHand)




count = [0, 0, 0]
for i in range(0, 500000):
    if i % 50000 == 0 and i != 0:
        print(count, "\tWinning percentage: ", (count[0]/(count[0]+count[2])*100))
        count = [0, 0, 0]

    result = episode(tableActiveAce, tableInactiveAce)
    if result == 1:
        count[0] += 1
    elif result == 0:
        count[1] += 1
    else:
        count[2] += 1

print()
print("Table using Ace as 11:")
utils.printSAV(tableInactiveAce)
print()
print("Table using Ace as 1:")
utils.printSAV(tableActiveAce)