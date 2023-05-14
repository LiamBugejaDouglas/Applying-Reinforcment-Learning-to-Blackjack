import random
from re import L
import envUtils as utils

def updateSAV(tableActiveAce, tableInactiveAce, dealerCard, qList, reward):
    if qList[0][2]:
        if qList[0][1] == 'hitValue':
            a = 1/(tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitCount"] + 1)
            if qList[1][1]:
                tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"] += a * (reward + tableActiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"])
            else:
                tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"] += a * (reward + tableInactiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"])
        else:
            a = 1/(tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standCount"] + 1)
            if qList[1][1]:
                tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"] += a * (reward + tableActiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"])
            else:
                tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"] += a * (reward + tableInactiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableActiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"])
    else:
        if qList[0][1] == 'hitValue':
            a = 1/(tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitCount"] + 1)
            if qList[1][1]:
                tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"] += a * (reward + tableActiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"])
            else:
                tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"] += a * (reward + tableInactiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["hitValue"])
        else:
            a = 1/(tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standCount"] + 1)
            if qList[1][1]:
                tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"] += a * (reward + tableActiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"])
            else:
                tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"] += a * (reward + tableInactiveAce[qList[1][0]][utils.getCardValue(dealerCard)][qList[1][1]] - tableInactiveAce[qList[0][0]][utils.getCardValue(dealerCard)]["standValue"])

def randomChoice(deck, stateActionValues, playerCards, dealerCard, cardsSum):
    # 50-50 random value 
    stand = bool(random.getrandbits(1))
    
    if stand:
        stateActionValues[cardsSum][dealerCard]["standCount"] += 1
        return True
    
    stateActionValues[cardsSum][dealerCard]["hitCount"] += 1
    return False

def findMax(stateActionValues, dealerCard, cardsSum):
    if stateActionValues[cardsSum][dealerCard]["hitValue"] < stateActionValues[cardsSum][dealerCard]["standValue"]: 
        # stand > hit
        return [cardsSum, "standValue", utils.ace]
    
    elif stateActionValues[cardsSum][dealerCard]["hitValue"] > stateActionValues[cardsSum][dealerCard]["standValue"]:
        # hit > stand
        return [cardsSum, "hitValue", utils.ace]

    else:
        # hit = stand; random choice
        stand = bool(random.getrandbits(1))
        if stand:
            return [cardsSum, "standValue", utils.ace]
        else:
            return [cardsSum, "hitValue", utils.ace]

def completeAction(deck, tableActiveAce, tableInactiveAce, playerCards, dealerCard, epsilon):
    cardsSum = utils.sumOfCards(playerCards)
    currentQ = list()
    newQ = list()

    while cardsSum < 21:
        # in case a hit lead to changing an ace's value
        if utils.ace:
            stateActionValues = tableActiveAce
        else:
            stateActionValues = tableInactiveAce
        
        # update q(s, a) of previous state
        if len(currentQ):
            newQ = findMax(stateActionValues, dealerCard, cardsSum)
            updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, newQ], 0)

        ran = random.randint(0, 1000) / 1000
        if ran < epsilon:
            if randomChoice(deck, stateActionValues, playerCards, dealerCard, cardsSum):
                # STAND action
                return [cardsSum, "standValue", utils.ace]
            
            # HIT action
            currentQ = [cardsSum, "hitValue", utils.ace]

            # update hand and sum
            playerCards.append(deck.pop())
            cardsSum = utils.sumOfCards(playerCards)
        
        else:
            if stateActionValues[cardsSum][dealerCard]["hitValue"] < stateActionValues[cardsSum][dealerCard]["standValue"]: 
                # STAND > HIT
                return [cardsSum, "standValue", utils.ace]

            elif stateActionValues[cardsSum][dealerCard]["hitValue"] > stateActionValues[cardsSum][dealerCard]["standValue"]: 
                # HIT > STAND
                currentQ = [cardsSum, "hitValue", utils.ace]

                # upadte hadn and sum
                playerCards.append(deck.pop())
                cardsSum = utils.sumOfCards(playerCards)
            
            else:
                # action values are equal, hence random choice
                if randomChoice(deck, stateActionValues, playerCards, dealerCard, cardsSum):
                    # STAND
                    return [cardsSum, "standValue", utils.ace]

                # HIT
                currentQ = [cardsSum, "hitValue", utils.ace]

                # update hand and sum
                playerCards.append(deck.pop())
                cardsSum = utils.sumOfCards(playerCards)

    return currentQ
        

def qLearning(deck, tableActiveAce, tableInactiveAce, playerCards, dealerCards, epsilon):
    if utils.sumOfCards(playerCards) == 21:
        return    

    q = completeAction(deck, tableActiveAce, tableInactiveAce, playerCards, utils.getCardValue(dealerCards[0]), epsilon)
    reward = utils.reward(playerCards, dealerCards)

    # update final q(s, a) where q(s', a') = q(s, a)
    updateSAV(tableActiveAce, tableInactiveAce, dealerCards[0], [q, q], reward)

