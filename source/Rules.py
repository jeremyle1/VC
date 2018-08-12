from source.Card import Card

def double(cards):
    """Returns true if length of cards is 2 and both have the same rank."""
    return len(cards) == 2 and all(card.rank == cards[0].rank for card in cards)

def triple(cards):
    """Returns true if length of cards is 3 and all have the same rank."""
    return len(cards) == 3 and all(card.rank == cards[0].rank for card in cards)

def quad(cards):
    """Returns true if length of cards is 4 and all have the same rank."""
    return len(cards) == 4 and all(card.rank == cards[0].rank for card in cards)

def straight(cards):
    """Returns true if length of cards is from 3 to 12, and each card is one rank higher than the previous."""
    all_ranks = [str(n) for n in range(3, 11)] + list('JQKA')
    ranks = [card.rank for card in sorted(cards, key=Card.hearts_high)]

    try:
        first_rank = all_ranks.index(ranks[0])
        last_rank = all_ranks.index(ranks[-1])
        return 2 < len(cards) < 13 and all_ranks[first_rank:last_rank + 1] == ranks
    except ValueError:
        return False

def double_straight(cards):
    """Returns true if cards contains 3 or more pairs, with each pair being one rank higher than the previous."""
