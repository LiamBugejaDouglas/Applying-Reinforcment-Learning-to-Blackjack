import random
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

def completeAction(deck, tableActiveAce, tableInactiveAce, playerCards, dealerCard, epsilon):
    cardsSum = utils.sumOfCards(playerCards)
    currentQ = list()
    newQ = list()

    while cardsSum < 21:
        currentQ = newQ.copy()

        # in case a hit lead to changing an ace's value
        if utils.ace:
            stateActionValues = tableActiveAce
        else:
            stateActionValues = tableInactiveAce

        ran = random.randint(0, 1000) / 1000
        if ran < epsilon:
            if randomChoice(deck, stateActionValues, playerCards, dealerCard, cardsSum):
                # STAND action
                if len(currentQ):
                    updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, [cardsSum, 'standValue', utils.ace]], 0)
                return [cardsSum, 'standValue', utils.ace]

            # HIT action
            newQ = [cardsSum, 'hitValue', utils.ace]
            if len(currentQ):
                updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, newQ], 0)
                currentQ = newQ
            
            # update player cards
            playerCards.append(deck.pop())
            cardsSum = utils.sumOfCards(playerCards)
        
        else :
            if stateActionValues[cardsSum][dealerCard]["hitValue"] < stateActionValues[cardsSum][dealerCard]["standValue"]: 
                # if stand action value is largere than hit
            
                stateActionValues[cardsSum][dealerCard]["standCount"] += 1 # increment N(s, a)
                if len(currentQ): # update previous q(s, a)
                    updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, [cardsSum, 'standValue', utils.ace]], 0)

                return [cardsSum, 'standValue', utils.ace]
            
            elif stateActionValues[cardsSum][dealerCard]["hitValue"] > stateActionValues[cardsSum][dealerCard]["standValue"]:
                # if hit action value is largere the stand
                stateActionValues[cardsSum][dealerCard]["hitCount"] += 1

                newQ = [cardsSum, 'hitValue', utils.ace]
                if len(currentQ): # update previous q(s, a)
                    updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, newQ], 0)
                    currentQ = newQ

                # update player cards and sum
                playerCards.append(deck.pop())
                cardsSum = utils.sumOfCards(playerCards)

            else:
                # action values are equal, hence random choice
                if randomChoice(deck, stateActionValues, playerCards, dealerCard, cardsSum):

                    if len(currentQ): # update previous q(s, a)
                        updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, [cardsSum, 'standValue', utils.ace]], 0)

                    return [cardsSum, 'standValue', utils.ace]
                    
                # HIT action
                newQ = [cardsSum, 'hitValue', utils.ace]
                if len(currentQ): # update previous q(s, a)
                    updateSAV(tableActiveAce, tableInactiveAce, dealerCard, [currentQ, newQ], 0)
                    currentQ = newQ
                
                # update player cards
                playerCards.append(deck.pop())
                cardsSum = utils.sumOfCards(playerCards)

        cardsSum = utils.sumOfCards(playerCards)
    
    # in case there was a hit value that resulted in going over 21
    return newQ

def sarsa(deck, tableActiveAce, tableInactiveAce, playerCards, dealerCards, epsilon):
    if utils.sumOfCards(playerCards) == 21:
        return    

    q = completeAction(deck, tableActiveAce, tableInactiveAce, playerCards, utils.getCardValue(dealerCards[0]), epsilon)
    reward = utils.reward(playerCards, dealerCards)

    # update final q(s, a) where q(s', a') = q(s, a)
    updateSAV(tableActiveAce, tableInactiveAce, dealerCards[0], [q, q], reward)
