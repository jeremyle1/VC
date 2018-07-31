from source.Card import Card
import unittest

class TestCard(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(ValueError):
            card = Card('5', 'Hearts')
        with self.assertRaises(ValueError):
            card = Card('5', 'diamond')
        with self.assertRaises(ValueError):
            card = Card('5', 'club')

    def test_hearts_high(self):
        card1 = Card('3', 'spades')
        card2 = Card('2', 'hearts')
        card3 = Card('8', 'diamonds')

        self.assertEqual(card1.hearts_high(), 0)
        self.assertEqual(card2.hearts_high(), 51)
        self.assertEqual(card3.hearts_high(), 22)

    def test_toggle_selected(self):
        card = Card('5', 'hearts')
        if card.is_selected():
            card.toggle_selected()
            self.assertEqual(card.is_selected(), False)
        else:
            card.toggle_selected()
            self.assertEqual(card.is_selected(), True)

    def test_is_selected(self):
        card = Card('5', 'hearts')
        self.assertEqual(card.is_selected(), card.selected)

if __name__ == '__main__':
    unittest.main()