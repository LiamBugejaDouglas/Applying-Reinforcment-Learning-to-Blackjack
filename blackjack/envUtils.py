import random

# False if ace counts as 11
# True if ace counts as 1
ace = False

def getCardValue(card):
    if card == 'J' or card == 'Q' or card == 'K':
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def createStateActionValue():
    stateActionValues = dict()

    for i in range(12, 21):
        tempDict = dict()
        for j in range(2, 12):
            tempDict[j] = {
                "hitValue" : 0,
                "standValue" : 0,
                "hitCount" : 0,
                "standCount" : 0
            }

        stateActionValues[i] = tempDict

    return stateActionValues

def createDeck():
    cards =  ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = list()

    for i in cards:
        for j in range(4):
            deck.append(i)

    random.shuffle(deck)

    return deck

def sumOfCards(hand):
    global ace
    aceFlag = False
    cardsSum = 0


    for i in hand:
        if i == 'J' or i == 'Q' or i == 'K': # jack, queen and king have a value of 10
            cardValue = 10

        elif i == 'A': # ace can have a value of 11
            cardValue = 11
            aceFlag = True
        else:
            cardValue = int(i)

        cardsSum += cardValue

    # if the sum of cards exceeds 21 whilst holding an ace, change the ace to a value of 1
    if cardsSum > 21 and aceFlag:
        cardsSum -= 10
        ace = True

    return cardsSum

def printHand(hand):
    for i in hand:
        print(i, end=" ")
    
    print("\tSum: ", sumOfCards(hand))

def printSAV(table):
    # Header Row
    print(" {:<7}".format(' '), end="")
    for i in range(2, 12):
        if i == 11:
            print("{:<7}".format('A'))
        else :
            print("{:<7} ".format(str(i)), end="")

    for i in table:
        print("{:<7} ".format(str(i)), end="")
        for j in table[i]:
            if table[i][j]["hitValue"] > table[i][j]["standValue"]:
                print("{:<7} ".format("HIT"), end="")
            else:
                print("{:<7} ".format("STAND"), end="")

        print()

def result(playerHand, dealerHand):
    if sumOfCards(playerHand) > 21:
        print("THE DEALER WON\nThe agent exceeded the sum of 21.\n")
        print("Player's Hand:", end=" ")
        printHand(playerHand)
        print("Dealer's Hand:", end=" ")
        printHand(dealerHand)

    elif sumOfCards(dealerHand) > sumOfCards(playerHand):
        print("THE DEALER WON\nThe dealer has a higher sum of cards than the agent.\n")
        print("Player's Hand:", end=" ")
        printHand(playerHand)
        print("Dealer's Hand:", end=" ")
        printHand(dealerHand)

    elif sumOfCards(dealerHand) > 21:
        print("THE AGENT WON\nThe dealer exceeded the sum of 21.\n")
        print("Player's Hand:", end=" ")
        printHand(playerHand)
        print("Dealer's Hand:", end=" ")
        printHand(dealerHand)

    elif sumOfCards(dealerHand) < sumOfCards(playerHand):
        print("THE AGENT WON\nThe agent has a higher sum of cards than the dealer.\n")
        print("Player's Hand:", end=" ")
        printHand(playerHand)
        print("Dealer's Hand:", end=" ")
        printHand(dealerHand)

    elif sumOfCards(dealerHand) == sumOfCards(playerHand):
        print("DRAW\n")
        print("Player's Hand:", end=" ")
        printHand(playerHand)
        print("Dealer's Hand:", end=" ")
        printHand(dealerHand)

def reward(playerHand, dealerHand):
    playerSum = sumOfCards(playerHand)
    dealerSum = sumOfCards(dealerHand)

    if playerSum > 21:
        return -1

    if dealerSum > 21:
        return 1

    if dealerSum > playerSum:
        # agent lost
        return -1

    elif playerSum > dealerSum:
        # agent won
        return 1
        
    
    else:
        # draw
        return 0