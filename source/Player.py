from source.Card import Card

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.hand = []
        # milliseconds to pause when AI's turn.
        self.thinking_time = 1500

    def printCards(self):
        for card in self.hand:
            print(card.rank, card.suit)

    def get_new_hand(self, deck):
        self.hand = sorted(deck.deal_hand(), key=Card.hearts_high)

    def has_3_spades(self):
        """Returns true if player has 3 of spades in their hand."""
        if Card('3', 'spades') in self.hand:
            return True
        return False
