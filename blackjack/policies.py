import envUtils as utils

def dealerPolicy(deck, hand):
    # dealer keeps hitting until he exceeds 17
    while utils.sumOfCards(hand) < 17:
        hand.append(deck.pop())

def playerPolicy(deck, hand):
    while utils.sumOfCards(hand) < 12:
        hand.append(deck.pop())

    if utils.sumOfCards(hand) > 20:
        return

