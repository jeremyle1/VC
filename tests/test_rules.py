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

    def test_beats(self):
        # Singles
        self.assertEqual(Rules.beats([Card(3, 'spades')], [Card(3, 'spades')]), False)
        self.assertEqual(Rules.beats([Card(3, 'spades')], [Card(2, 'spades')]), True)
        self.assertEqual(Rules.beats([Card(3, 'clubs')], [Card(3, 'spades')]), False)
        self.assertEqual(Rules.beats([Card(3, 'spades')], [Card('J', 'hearts')]), True)
        self.assertEqual(Rules.beats([], []), False)
        quad_chop = [Card('3', suit) for suit in suits]
        self.assertEqual(Rules.beats([Card(2, 'hearts')], quad_chop), True)
        dbl_straight_chop = [Card(3, 'spades'), Card(3, 'clubs'), Card(4, 'diamonds'), Card(4, 'hearts'),
                             Card(5, 'clubs'), Card(5, 'diamonds')]
        self.assertEqual(Rules.beats([Card(2, 'spades')], dbl_straight_chop), True)
        # Doubles
        cards1 = [Card(3, 'spades'), Card(3, 'diamonds')]
        cards2 = [Card(3, 'clubs'), Card(3, 'hearts')]
        self.assertEqual(Rules.beats(cards1, cards2), True)
        cards3 = [Card(3, 'clubs'), Card(3, 'hearts')]
        cards4 = [Card(4, 'clubs'), Card(4, 'hearts')]
        self.assertEqual(Rules.beats(cards3, cards4), True)
        cards5 = [Card(2, 'clubs'), Card(2, 'hearts')]
        cards6 = [Card('A', 'clubs'), Card('A', 'hearts')]
        self.assertEqual(Rules.beats(cards5, cards6), False)
        cards7 = [Card('Q', 'clubs'), Card('Q', 'hearts')]
        cards8 = [Card('Q', 'clubs'), Card('Q', 'diamonds')]
        self.assertEqual(Rules.beats(cards7, cards8), False)
        cards9 = [Card('Q', 'clubs'), Card('J', 'hearts')]
        cards10 = [Card('Q', 'clubs'), Card('J', 'diamonds')]
        self.assertEqual(Rules.beats(cards9, cards10), False)
        # Triples
        cards9 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'spades')]
        cards10 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'hearts')]
        self.assertEqual(Rules.beats(cards9, cards10), True)
        cards11 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'hearts')]
        cards12 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'hearts')]
        self.assertEqual(Rules.beats(cards11, cards12), False)
        cards13 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades')]
        cards14 = [Card('10', 'hearts'), Card('10', 'diamonds'), Card('10', 'spades')]
        self.assertEqual(Rules.beats(cards13, cards14), True)
        cards13 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades')]
        cards14 = [Card('7', 'hearts'), Card('7', 'diamonds'), Card('7', 'spades')]
        self.assertEqual(Rules.beats(cards13, cards14), False)
        cards15 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades')]
        cards16 = [Card('A', 'hearts'), Card('10', 'diamonds'), Card('A', 'spades')]
        self.assertEqual(Rules.beats(cards15, cards16), False)
        # Quads
        cards17 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'spades'), Card('Q', 'spades')]
        cards18 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'spades'), Card('Q', 'hearts')]
        self.assertEqual(Rules.beats(cards17, cards18), True)
        cards19 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'hearts'), Card('Q', 'hearts')]
        cards20 = [Card('Q', 'clubs'), Card('Q', 'diamonds'), Card('Q', 'hearts'), Card('Q', 'hearts')]
        self.assertEqual(Rules.beats(cards19, cards20), False)
        cards21 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades'), Card('9', 'clubs')]
        cards22 = [Card('10', 'hearts'), Card('10', 'diamonds'), Card('10', 'spades'), Card('10', 'clubs')]
        self.assertEqual(Rules.beats(cards21, cards22), True)
        cards23 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades'), Card('9', 'clubs')]
        cards24 = [Card('7', 'hearts'), Card('7', 'diamonds'), Card('7', 'spades'), Card('7', 'clubs')]
        self.assertEqual(Rules.beats(cards23, cards24), False)
        cards25 = [Card('9', 'hearts'), Card('9', 'diamonds'), Card('9', 'spades'), Card('9', 'clubs')]
        cards26 = [Card('A', 'hearts'), Card('10', 'diamonds'), Card('A', 'spades'), Card('A', 'clubs')]
        self.assertEqual(Rules.beats(cards25, cards26), False)


if __name__ == '__main__':
    unittest.main()
