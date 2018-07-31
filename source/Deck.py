import random
from source.Card import Card

class Deck:
    def __init__(self):
        self.__set_cards()

    def __set_cards(self):
        """
        Initialize list of 52 cards
        """
        self.cards = [Card(rank, suit) for rank in Card.ranks for suit in Card.suits]
        self.undealtCards = self.cards[:]

    def print_cards(self):
        for card in self.cards:
            print(card.rank, card.suit)

    def deal_hand(self):
        """
        Returns list of 13 un-dealt cards
        """
        hand = []
        for _ in range(0, 13):
            card = random.choice(self.undealtCards)
            hand.append(card)
            self.undealtCards.remove(card)

        return hand
