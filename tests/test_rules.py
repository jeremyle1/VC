import unittest
from source.Card import Card
from source import Rules

ranks = [str(n) for n in range(3, 11)] + list('JQKA2')
class TestRules(unittest.TestCase):
    def test_double(self):
        cards1 = [Card('3', 'spades'), Card('3', 'hearts')]
        cards2 = [Card('A', 'spades'), Card('A', 'spades')]
        cards3 = [Card('3', 'spades'), Card('2', 'hearts')]
        cards4 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        cards6 = [Card(2, 'spades')]
        self.assertEqual(Rules.double(cards1), True)
        self.assertEqual(Rules.double(cards2), True)
        self.assertEqual(Rules.double(cards3), False)
        self.assertEqual(Rules.double(cards4), False)
        self.assertEqual(Rules.double(cards6), False)

    def test_triple(self):
        cards1 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        cards2 = [Card('2', 'spades'), Card('2', 'hearts'), Card('2', 'diamonds')]
        cards3 = [Card('2', 'spades'), Card('2', 'spades'), Card('3', 'spades')]
        self.assertEqual(Rules.triple(cards1), True)
        self.assertEqual(Rules.triple(cards2), True)
        self.assertEqual(Rules.triple(cards3), False)

    def test_quad(self):
        cards1 = [Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades'), Card('2', 'spades')]
        cards2 = [Card('2', 'clubs'), Card('2', 'spades'), Card('2', 'diamonds'), Card('2', 'hearts')]
        cards3 = [Card('2', 'clubs'), Card('2', 'spades'), Card('2', 'diamonds'), Card('A', 'hearts')]
        self.assertEqual(Rules.quad(cards1), True)
        self.assertEqual(Rules.quad(cards2), True)
        self.assertEqual(Rules.quad(cards3), False)

    def test_straight(self):
        cards1 = [Card(rank, 'spades') for rank in ranks[0:12]]
        cards2 = [Card(rank, 'spades') for rank in ranks]
        cards3 = [Card(rank, 'spades') for rank in ranks[0:2]]
        cards4 = [Card(rank, 'spades') for rank in ranks[0:3]]
        cards5 = cards1[::-1]
        cards6 = cards2[::-1]
        cards7 = cards4[::-1]
        self.assertEqual(Rules.straight(cards1), True)
        self.assertEqual(Rules.straight(cards2), False)
        self.assertEqual(Rules.straight(cards3), False)
        self.assertEqual(Rules.straight(cards4), True)
        self.assertEqual(Rules.straight(cards5), True)
        self.assertEqual(Rules.straight(cards6), False)
        self.assertEqual(Rules.straight(cards7), True)

if __name__ == '__main__':
    unittest.main()
