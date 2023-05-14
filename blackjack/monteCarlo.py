import random
import numpy as np

import envUtils as utils

def randomChoice(deck, stateActionValues, playerCards, dealerCard, visitedSAV, cardsSum):
    # 50-50 random value 
    stand = bool(random.getrandbits(1))
    
    if stand:
        stateActionValues[cardsSum][dealerCard]["standCount"] += 1
        visitedSAV.append([cardsSum, 'standValue', utils.ace])
        return True
    
    stateActionValues[cardsSum][dealerCard]["hitCount"] += 1
    visitedSAV.append([cardsSum, 'hitValue', utils.ace])

    # update player hand and sum
    playerCards.append(deck.pop())
    cardsSum = utils.sumOfCards(playerCards)

    return False

def completeActions(deck, tableActiveAce, tableInactiveAce, playerCards, dealerCard, exploringStart, epsilon):
    visitedSAV = list() 
    cardsSum = utils.sumOfCards(playerCards)

    # checking which table to use
    if utils.ace:
        stateActionValues = tableActiveAce
    else:
        stateActionValues = tableInactiveAce


    if cardsSum == 21:
        return visitedSAV

    if exploringStart:

        # first random state
        if randomChoice(deck, stateActionValues, playerCards, dealerCard, visitedSAV, cardsSum):
            return visitedSAV

        cardsSum = utils.sumOfCards(playerCards)

        # in case a hit lead to changing an ace's value
        if utils.ace:
            stateActionValues = tableActiveAce
        else:
            stateActionValues = tableInactiveAce


    while cardsSum < 21:

        ran = random.randint(0, 1000) / 1000
        if ran < epsilon:
            # random value between 0 and 1 is smaller than epsilon, hence random choice
            if randomChoice(deck, stateActionValues, playerCards, dealerCard, visitedSAV, cardsSum):
               return visitedSAV

        else:
            if stateActionValues[cardsSum][dealerCard]["hitValue"] < stateActionValues[cardsSum][dealerCard]["standValue"]:
                # if stand action value is largere than hit
                stateActionValues[cardsSum][dealerCard]["standCount"] += 1
                visitedSAV.append([cardsSum, 'standValue', utils.ace])
                return visitedSAV

            elif stateActionValues[cardsSum][dealerCard]["hitValue"] > stateActionValues[cardsSum][dealerCard]["standValue"]:
                # if hit action value is largere the stand
                stateActionValues[cardsSum][dealerCard]["hitCount"] += 1
                visitedSAV.append([cardsSum, 'hitValue', utils.ace])

                # update player cards and sum
                playerCards.append(deck.pop())
                cardsSum = utils.sumOfCards(playerCards)

            else:
                # action values are equal, hence random choice
                if randomChoice(deck, stateActionValues, playerCards, dealerCard, visitedSAV, cardsSum):
                    return visitedSAV


        cardsSum = utils.sumOfCards(playerCards)
        # in case a hit lead to changing an ace's value
        if utils.ace:
            stateActionValues = tableActiveAce
        else:
            stateActionValues = tableInactiveAce

    return visitedSAV

def updateSAV(tableActiveAce, tableInactiveAce, visitedSAV, visibleDealerCard, reward):
    while len(visitedSAV):
        for i in visitedSAV:
            if i[2]:
                if i[1] == 'hitValue':
                    tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitValue"] += (1/tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitCount"]) * ((reward/len(visitedSAV)) - tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitValue"])
                else:
                    tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standValue"] += (1/tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standCount"]) * ((reward/len(visitedSAV)) - tableActiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standValue"])
            else:
                if i[1] == 'hitValue':
                    tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitValue"] += (1/tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitCount"]) * ((reward/len(visitedSAV)) - tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["hitValue"])
                else:
                    tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standValue"] += (1/tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standCount"]) * ((reward/len(visitedSAV)) - tableInactiveAce[i[0]][utils.getCardValue(visibleDealerCard)]["standValue"])

        visitedSAV.pop(0)

def monteCarlo(deck, tableActiveAce, tableInactiveAce, visitedSAV, playerHand, dealerHand, exploringStart, epsilon):
    # completes the actions usin
    visitedSAV = completeActions(deck, tableActiveAce, tableInactiveAce, playerHand, utils.getCardValue(dealerHand[0]), exploringStart, epsilon)

    updateSAV(tableActiveAce, tableInactiveAce, visitedSAV, dealerHand[0], utils.reward(playerHand, dealerHand))