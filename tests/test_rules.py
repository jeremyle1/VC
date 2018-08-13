import unittest
from source.Card import Card
from source import Rules
import random

ranks = [str(n) for n in range(3, 11)] + list('JQKA2')
suits = ['spades', 'clubs', 'diamonds', 'hearts']
class TestRules(unittest.TestCase):
    def test_double(self):
        self.assertEqual(Rules.double([]), False)
        cards1 = [Card('3', 'spades'), Card('3', 'hearts')]
        self.assertEqual(Rules.double(cards1), True)
        cards2 = [Card('A', 'spades'), Card('A', 'spades')]
        self.assertEqual(Rules.double(cards2), True)
        cards3 = [Card('3', 'spades'), Card('2', 'hearts')]
        self.assertEqual(Rules.double(cards3), False)
        cards4 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        self.assertEqual(Rules.double(cards4), False)
        cards6 = [Card(2, 'spades')]
        self.assertEqual(Rules.double(cards6), False)

    def test_triple(self):
        self.assertEqual(Rules.triple([]), False)
        cards1 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        self.assertEqual(Rules.triple(cards1), True)
        cards2 = [Card('2', 'spades'), Card('2', 'hearts'), Card('2', 'diamonds')]
        self.assertEqual(Rules.triple(cards2), True)
        cards3 = [Card('2', 'spades'), Card('2', 'spades'), Card('3', 'spades')]
        self.assertEqual(Rules.triple(cards3), False)

    def test_quad(self):
        self.assertEqual(Rules.quad([]), False)
        cards1 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        self.assertEqual(Rules.quad(cards1), True)
        cards2 = [Card('2', 'clubs'), Card('2', 'spades'), Card('2', 'diamonds'), Card('2', 'hearts')]
        self.assertEqual(Rules.quad(cards2), True)
        cards3 = [Card('2', 'clubs'), Card('2', 'spades'), Card('2', 'diamonds'), Card('A', 'hearts')]
        self.assertEqual(Rules.quad(cards3), False)

    def test_straight(self):
        self.assertEqual(Rules.straight([]), False)
        cards1 = [Card(rank, 'spades') for rank in ranks[0:12]]
        self.assertEqual(Rules.straight(cards1), True)
        cards2 = [Card(rank, 'spades') for rank in ranks]
        self.assertEqual(Rules.straight(cards2), False)
        cards3 = [Card(rank, 'spades') for rank in ranks[0:2]]
        self.assertEqual(Rules.straight(cards3), False)
        cards4 = [Card(rank, 'spades') for rank in ranks[0:3]]
        self.assertEqual(Rules.straight(cards4), True)
        cards5 = cards1[::-1]
        self.assertEqual(Rules.straight(cards5), True)
        cards6 = cards2[::-1]
        self.assertEqual(Rules.straight(cards6), False)
        cards7 = cards4[::-1]
        self.assertEqual(Rules.straight(cards7), True)
        cards8 = [Card(rank, 'spades') for rank in ranks[10:13]]
        self.assertEqual(Rules.straight(cards8), False)
        cards9 = [Card(rank, 'spades') for rank in ranks[9:12]]
        self.assertEqual(Rules.straight(cards9), True)

    def test_double_straight(self):
        self.assertEqual(Rules.double_straight([]), False)
        cards1 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 4, 5, 5]]
        self.assertEqual(Rules.double_straight(cards1), True)
        cards2 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 5, 5, 5]]
        self.assertEqual(Rules.double_straight(cards2), False)
        cards3 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 4, 5, 5, 6, 6]]
        self.assertEqual(Rules.double_straight(cards3), True)
        cards4 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 4]]
        self.assertEqual(Rules.double_straight(cards4), False)
        cards5 = [Card(rank, random.choice(suits)) for rank in [3, 3]]
        self.assertEqual(Rules.double_straight(cards5), False)
        cards6 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 4, 5, 5, 6, 6, 8, 8]]
        self.assertEqual(Rules.double_straight(cards6), False)
        cards7 = [Card(rank, random.choice(suits)) for rank in ['Q', 'Q', 'K', 'K', 'A', 'A']]
        self.assertEqual(Rules.double_straight(cards7), True)
        cards8 = [Card(rank, random.choice(suits)) for rank in ['K', 'K', 'A', 'A', 2, 2]]
        self.assertEqual(Rules.double_straight(cards8), False)
        cards9 = [Card(rank, random.choice(suits)) for rank in [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,
                                                                'J', 'J', 'Q', 'Q', 'K', 'K', 'A', 'A']]
        self.assertEqual(Rules.double_straight(cards9), True)

if __name__ == '__main__':
    unittest.main()
