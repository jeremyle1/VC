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
        # Straights
        cards27 = [Card('3', 'spades'), Card('4', 'clubs'), Card('5', 'diamonds')]
        cards28 = [Card('3', 'spades'), Card('4', 'clubs'), Card('5', 'hearts')]
        self.assertEqual(Rules.beats(cards27, cards28), True)
        cards29 = [Card('3', 'spades'), Card('4', 'clubs'), Card('5', 'diamonds')]
        cards30 = [Card('3', 'spades'), Card('4', 'clubs'), Card('5', 'diamonds')]
        self.assertEqual(Rules.beats(cards29, cards30), False)
        cards31 = [Card('3', 'spades'), Card('4', 'clubs'), Card('5', 'diamonds')]
        cards32 = [Card('K', 'spades'), Card('A', 'clubs'), Card('2', 'hearts')]
        self.assertEqual(Rules.beats(cards31, cards32), False)
        cards33 = [Card('Q', 'spades'), Card('K', 'clubs'), Card('A', 'hearts')]
        cards34 = [Card('K', 'spades'), Card('A', 'clubs'), Card('2', 'spades')]
        self.assertEqual(Rules.beats(cards33, cards34), False)
        # Double Straights
        cards35 = [Card(rank, 'spades') for rank in [3,3,4,4,5,5]]
        cards36 = [Card(rank, 'spades') for rank in [4,4,5,5,6,6]]
        self.assertEqual(Rules.beats(cards35, cards36), True)
        cards35 = [Card(rank, 'spades') for rank in [3, 3, 4, 4, 5, 5]]
        cards36 = [Card(rank, 'spades') for rank in [4, 4, 5, 5, 7, 7]]
        self.assertEqual(Rules.beats(cards35, cards36), False)
        cards37 = [Card(rank, 'spades') for rank in [3, 3, 4, 4, 5, 5]]
        cards38 = [Card(rank, 'spades') for rank in ['K', 'K', 'A', 'A', 2, 2]]
        self.assertEqual(Rules.beats(cards37, cards38), False)
        cards39 = [Card(rank, 'spades') for rank in [3, 3, 4, 4, 5, 5]]
        cards40 = [Card(rank, 'spades') for rank in [3, 3, 4, 4]]
        cards40.extend([Card('5', 'spades'), Card('5', 'clubs')])
        self.assertEqual(Rules.beats(cards39, cards40), True)

    def test_possible_moves(self):
        # Singles
        single1 = [Card('3', 'spades')]
        single2 = [Card('3', 'clubs'), Card('4', 'spades'), Card('A', 'diamonds'), Card('2', 'spades')]
        self.assertEqual(Rules.possible_moves(single1, single2), [[card] for card in single2])
        single3 = [Card('2', 'hearts')]
        single4 = [Card('3', 'clubs'), Card('4', 'spades'), Card('A', 'diamonds'), Card('2', 'spades')]
        self.assertEqual(Rules.possible_moves(single3, single4), [])
        single5 = [Card('2', 'spades')]
        single6 = [Card('2', 'clubs'), Card('2', 'hearts'), Card('3', 'spades'), Card('3', 'clubs'),
                   Card('4', 'spades'), Card('4', 'clubs'), Card('5', 'spades'), Card('5', 'clubs')]
        self.assertEqual(Rules.possible_moves(single5, single6), [[Card('2', 'clubs')], [Card('2', 'hearts')],
                                                                  single6[2:]])

        # Doubles
        double1 = [Card('3', 'clubs'), Card('3', 'hearts')]
        double2 = [Card('4', 'spades'), Card('4', 'clubs'), Card('5', 'diamonds'), Card('5', 'hearts')]
        self.assertEqual(Rules.possible_moves(double1, double2),
                         [[Card('4', 'spades'), Card('4', 'clubs')], [Card('5', 'diamonds'), Card('5', 'hearts')]])
        double3 = [Card('3', 'clubs'), Card('3', 'hearts')]
        double4 = [Card('4', 'spades'), Card('5', 'clubs'), Card('6', 'diamonds'), Card('7', 'hearts')]
        self.assertEqual(Rules.possible_moves(double3, double4), [])
        double5 = [Card('2', 'spades'), Card('2', 'clubs')]
        double6 = [Card('2', 'clubs'), Card('2', 'diamonds'), Card('2', 'hearts')]
        self.assertEqual(Rules.possible_moves(double5, double6), [[Card('2', 'clubs'), Card('2', 'diamonds')],
                        [Card('2', 'clubs'), Card('2', 'hearts')], [Card('2', 'diamonds'), Card('2', 'hearts')]])
        double7 = [Card('2', 'spades'), Card('2', 'clubs')]
        double8 = [Card('2', 'diamonds'), Card('2', 'hearts'), Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'),
                   Card('4', 'clubs'), Card('5', 'spades'), Card('5', 'clubs'), Card('6', 'spades'), Card('6', 'clubs'),
                   Card('7', 'spades'), Card('7', 'clubs')]
        self.assertEqual(Rules.possible_moves(double7, double8), [[Card('2', 'diamonds'), Card('2', 'hearts')],
                                                                  double8[2:-2], double8[4:]])

        # Triples
        triple1 = [Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        triple2 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('7', 'hearts')]
        self.assertEqual(Rules.possible_moves(triple1, triple2),
                         [[Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds')]])
        triple3 = [Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        triple4 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'),
                   Card('7', 'hearts'), Card('7', 'diamonds'), Card('7', 'spades')]
        self.assertEqual(Rules.possible_moves(triple3, triple4),
                         [[Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds')],
                          [Card('7', 'spades'), Card('7', 'diamonds'), Card('7', 'hearts')]])
        triple5 = [Card('2', 'spades'), Card('2', 'clubs'), Card('2', 'diamonds')]
        triple6 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'), Card('5', 'spades')
                   , Card('5', 'clubs'), Card('6', 'spades'), Card('6', 'clubs'), Card('7', 'spades'), Card('7', 'clubs')]
        self.assertEqual(Rules.possible_moves(triple5, triple6), [triple6[:]])
        triple7 = [Card('2', 'spades'), Card('2', 'clubs'), Card('2', 'diamonds')]
        triple8 = [Card('2', 'spades'), Card('2', 'diamonds'), Card('2', 'hearts'), Card('3', 'spades'),
                   Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'), Card('5', 'spades'), Card('5', 'clubs'),
                   Card('6', 'spades'), Card('6', 'clubs'), Card('7', 'spades'), Card('7', 'clubs')]
        self.assertEqual(Rules.possible_moves(triple7, triple8), [triple8[0:3], triple8[3:]])

        # Quads
        quad1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        quad2 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts')]
        self.assertEqual(Rules.possible_moves(quad1, quad2),
                         [[Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts')]])
        quad3 = [Card('3', 'spades'), Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        quad4 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds')]
        self.assertEqual(Rules.possible_moves(quad3, quad4), [])
        quad5 = [Card('3', 'spades'), Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        quad6 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('5', 'hearts')]
        self.assertEqual(Rules.possible_moves(quad5, quad6), [])
        quad7 = [Card('3', 'spades'), Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        quad8 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts'),
                 Card('5', 'clubs')]
        self.assertEqual(Rules.possible_moves(quad7, quad8),
                         [[Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts')]])
        quad9 = [Card('3', 'spades'), Card('3', 'clubs'), Card('3', 'diamonds'), Card('3', 'hearts')]
        quad10 = [Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts'),
                  Card('7', 'spades'), Card('7', 'clubs'), Card('7', 'diamonds'), Card('7', 'hearts')]
        self.assertEqual(Rules.possible_moves(quad9, quad10),
                         [[Card('4', 'spades'), Card('4', 'clubs'), Card('4', 'diamonds'), Card('4', 'hearts')],
                          [Card('7', 'spades'), Card('7', 'clubs'), Card('7', 'diamonds'), Card('7', 'hearts')]])

        # Straights
        straight1 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight2 = [Card('2', 'hearts')]
        self.assertEqual(Rules.possible_moves(straight1, straight2), [])
        straight3 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight4 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')]
        self.assertEqual(Rules.possible_moves(straight3, straight4),
                         [[Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')]])
        straight5 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight6 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts'), Card('5', 'diamonds')]
        self.assertEqual(Rules.possible_moves(straight5, straight6),
                         [[Card('3', 'spades'), Card('4', 'spades'), Card('5', 'diamonds')],
                          [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')]])
        straight7 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight8 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        self.assertEqual(Rules.possible_moves(straight7, straight8), [])
        straight9 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight10 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts'), Card('6', 'spades')]
        self.assertEqual(Rules.possible_moves(straight9, straight10),
                         [[Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')],
                          [Card('4', 'spades'), Card('5', 'hearts'), Card('6', 'spades')]])
        straight11 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight12 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts'), Card('7', 'spades')]
        self.assertEqual(Rules.possible_moves(straight11, straight12),
                         [[Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')]])
        straight13 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight14 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts'), Card('7', 'spades'),
                      Card('8', 'spades'), Card('9', 'spades')]
        self.assertEqual(Rules.possible_moves(straight13, straight14),
                         [[Card('3', 'spades'), Card('4', 'spades'), Card('5', 'hearts')],
                          [Card('7', 'spades'), Card('8', 'spades'), Card('9', 'spades')]])
        straight15 = [Card('3', 'spades'), Card('4', 'spades'), Card('5', 'spades')]
        straight16 = []
        self.assertEqual(Rules.possible_moves(straight15, straight16), [])

        # Double Straights
        dbl_straight_eq_len1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        dbl_straight_eq_len2 = [Card('3', 'diamonds'), Card('3', 'hearts'), Card('4', 'diamonds'), Card('4', 'hearts'),
                                   Card('5', 'diamonds'), Card('5', 'hearts')]
        self.assertEqual(Rules.possible_moves(dbl_straight_eq_len1, dbl_straight_eq_len2),
                         [dbl_straight_eq_len2])
        not_enough_cards1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        not_enough_cards2 = [Card('3', 'diamonds'), Card('3', 'hearts'), Card('4', 'diamonds'), Card('4', 'hearts'),
                                    Card('5', 'diamonds')]
        self.assertEqual(Rules.possible_moves(not_enough_cards1, not_enough_cards2), [])
        not_enough_cards3 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        not_enough_cards4 = [Card('3', 'diamonds')]
        self.assertEqual(Rules.possible_moves(not_enough_cards3, not_enough_cards4), [])
        three_rank_combinations1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        three_rank_combinations2 = [Card('3', 'diamonds'), Card('3', 'hearts'), Card('4', 'diamonds'), Card('4', 'hearts'),
                                   Card('5', 'clubs'), Card('5', 'diamonds'), Card('5', 'hearts')]
        self.assertEqual(Rules.possible_moves(three_rank_combinations1, three_rank_combinations2),
                         [three_rank_combinations2[:-1], three_rank_combinations2[:5] + three_rank_combinations2[-1:],
                          three_rank_combinations2[:4] + three_rank_combinations2[-2:]])
        four_ranks_of_pairs1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        four_ranks_of_pairs2 = [Card('3', 'diamonds'), Card('3', 'hearts'), Card('4', 'diamonds'), Card('4', 'hearts'),
                                   Card('5', 'diamonds'), Card('5', 'hearts'), Card('6', 'diamonds'), Card('6', 'hearts')]
        self.assertEqual(Rules.possible_moves(four_ranks_of_pairs1, four_ranks_of_pairs2),
                         [four_ranks_of_pairs2[:-2], four_ranks_of_pairs2[2:]])
        dbl_straight_with_two1 = [Card('3', 'spades'), Card('3', 'clubs'), Card('4', 'spades'), Card('4', 'clubs'),
                                   Card('5', 'spades'), Card('5', 'clubs')]
        dbl_straight_with_two2 = [Card('3', 'diamonds'), Card('3', 'hearts'), Card('4', 'diamonds'), Card('4', 'hearts'),
                                   Card('2', 'diamonds'), Card('2', 'hearts')]
        self.assertEqual(Rules.possible_moves(dbl_straight_with_two1, dbl_straight_with_two2), [])



if __name__ == '__main__':
    unittest.main()
