from source.Card import Card
import os

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
        # Get slice indices. A straight will have ranks that are a sub-sequence of all_ranks.
        first_rank = all_ranks.index(ranks[0])
        last_rank = all_ranks.index(ranks[-1])
        return 2 < len(cards) < 13 and all_ranks[first_rank:last_rank + 1] == ranks
    except IndexError:
        return False
    except ValueError:
        return False

def double_straight(cards):
    """Returns true if cards contains 3 or more pairs, with each pair being one rank higher than the previous."""
    if len(cards) % 2 == 1 or len(cards) < 6 or len(cards) > 24:
        return False
    cards_copy = sorted(cards, key=Card.hearts_high)

    # Return False if a pair of cards have differing ranks.
    for i in range(0, len(cards), 2):
        if not double([cards_copy[i], cards_copy[i+1]]):
            return False

    # Return True if the ranks of the doubles make a straight.
    return straight(cards_copy[::2])

def beats(cards1, cards2):
    """Returns true if cards2 can beat cards1.
        cards1, cards2: list of Card objects
    """
    cards1 = sorted(cards1, key=Card.hearts_high)
    cards2 = sorted(cards2, key=Card.hearts_high)
    if len(cards1) == 1:
        # Single 2 can be beaten by a double straight, a quad, or a higher 2.
        if cards1[0].rank == '2':
            if (len(cards2) == 6 and double_straight(cards2)) or quad(cards2):
                return True
        return len(cards2) == 1 and cards2[0].hearts_high() > cards1[0].hearts_high()
    elif double(cards1):
        # Double 2's can be beaten by a double straight with 4 pairs
        if cards1[0].rank == '2':
            if len(cards2) == 8 and double_straight(cards2):
                return True
        return double(cards2) and cards2[-1].hearts_high() > cards1[-1].hearts_high()
    elif triple(cards1):
        # Double 2's can be beaten by a double straight with 5 pairs
        if cards1[0].rank == '2':
            if len(cards2) == 10 and double_straight(cards2):
                return True
        return triple(cards2) and cards2[-1].hearts_high() > cards1[-1].hearts_high()
    elif quad(cards1):
        return quad(cards2) and cards2[-1].hearts_high() > cards1[-1].hearts_high()
    elif straight(cards1):
        # True if lengths are the same, both are straights, and last card of cards2 is greater than last card of cards1
        return len(cards1) == len(cards2) and straight(cards2) and cards2[-1].hearts_high() > cards1[-1].hearts_high()
    elif double_straight(cards1):
        return len(cards1) == len(cards2) and double_straight(cards2) and\
               cards2[-1].hearts_high() > cards1[-1].hearts_high()

    return False

def _find_doubles(cards1, cards2):
    """Find doubles in cards2 that can beat cards1.
    cards1: a list containing a pair of cards with the same rank.
    cards2: a list of cards."""
    moves = []
    for i in range(0, len(cards2) - 1):
        for j in range(i + 1, len(cards2)):
            if beats(cards1, [cards2[i], cards2[j]]):
                moves.append([cards2[i], cards2[j]])

    return moves

def _find_triples(cards1, cards2):
    """Find doubles in cards2 that can beat cards1.
        cards1: a list containing three cards with the same rank.
        cards2: a list of cards."""
    moves = []
    for i in range(0, len(cards2) - 2):
        for j in range(i + 1, len(cards2)-1):
            for k in range(j + 1, len(cards2)):
                if beats(cards1, [cards2[i], cards2[j], cards2[k]]):
                    moves.append([cards2[i], cards2[j], cards2[k]])

    return moves

def _find_quads(cards1, cards2):
    """Find quads in cards2 that can beat cards1.
    cards1: a list containing a four of a kind.
    cards2: a list of cards."""

    # Quads must be in a hand of at least 4 cards.
    if len(cards2) < 4:
        return []

    moves = []
    i = 0
    while i <= len(cards2):
        # Found a quad that can beat cards1.
        if beats(cards1, cards2[i:i+4]):
            moves.append(cards2[i:i+4])
            # The current 4 cards can't be apart of another quad.
            i = i + 4
        else:
            # Check for quad starting with the next card.
            i = i + 1

    return moves

def _find_straights(cards1, cards2):
    """Find straights in cards2 that can beat cards1.
    cards1: a sorted list of cards consisting of a straight.
    cards2: a sorted list of cards."""

    if len(cards2) < len(cards1):
        return []

    ranks = [str(n) for n in range(3, 11)] + list('JQKA')
    cards2_copy = [card for card in cards2 if card.rank != '2']
    moves = []
    straight_cards = []

    cards2_ranks = []
    current_rank = cards2_copy[0].rank
    same_ranks = []
    # Separate unique ranks into their own lists.
    for card in cards2_copy:
        # card has same rank as current_rank, append to same_ranks
        if card.rank == current_rank:
            same_ranks.append(card)
        # card has different rank than current_rank
        else:
            # Append list of cards with previous rank to cards2_ranks.
            cards2_ranks.append(same_ranks)
            # Update current_rank
            current_rank = card.rank
            same_ranks = [card]
            # Last card in cards2_copy.
        if card == cards2_copy[-1]:
            cards2_ranks.append(same_ranks)

    # Number of unique ranks of cards2 is less than length of cards1, or they are the same length but last rank is a 2.
    if (len(cards2_ranks) < len(cards1)) or (len(cards2_ranks) == len(cards1) and cards2_ranks[-1][0].rank == '2'):
        return []

    # Find cards that can make straights.
    for i in range(len(cards2_ranks)):
        # There are not enough remaining cards to make a straight.
        if(len(cards2_ranks)-i) < len(cards1):
            break

        # Lowest rank of straight must be equal to or greater than lowest rank of cards1
        if ranks.index(cards2_ranks[i][0].rank) < ranks.index(cards1[0].rank):
            continue

        temp_ranks = []
        # next len(cards1) ranks make up a straight.
        if straight([cards[0] for cards in cards2_ranks[i:i+len(cards1)]]):
            # first len(cards1)-1 ranks always belong to the straight
            temp_straight = cards2_ranks[i:i+len(cards1)-1]
            if temp_straight[0][0].rank == cards1[0].rank:
                # len(cards1) element of cards2_ranks has to have greater suit+rank than the last card of cards1.
                for card in cards2_ranks[i+len(cards1)-1]:
                    if card.hearts_high() > cards1[-1].hearts_high():
                        temp_ranks.append(card)
                temp_straight.append(temp_ranks)
                # Last cards of straight are greater than or equal to last card of cards1
                if temp_ranks:
                    straight_cards.append(temp_straight)
            # Last cards of straight are greater than or equal to last card of cards1
            else:
                temp_straight.append(cards2_ranks[i+len(cards1)-1])
                straight_cards.append(temp_straight)

    for s in straight_cards:
        moves.extend(_straight_combinations(s))

    return moves

def _straight_combinations(cards):
    """Returns a list of lists where each list contains Cards that make a straight. The length of each straight
        is the number of unique ranks in cards.

    cards: a list of list of Cards with length at least 3, where each succeeding Card is one rank higher than the
            previous.
            e.g. [[3,3], [4,4], [5], [6, 6]]"""

    temp = []
    if not cards:
        return [[]]
    else:
        for card in cards[0]:
            for combination in _straight_combinations(cards[1:]):
                temp.append([card] + combination)
        return temp


def possible_moves(cards1, cards2):
    """Returns a list of possible moves of cards2 hand that can beat cards1.
    cards1: list of Cards (valid move))
    cards2: list of cards (hand)"""

    cards1 = sorted(cards1, key=Card.hearts_high)
    cards2 = sorted(cards2, key=Card.hearts_high)
    moves = []
    if len(cards1) == 1:
        for card in cards2:
            if card.hearts_high() > cards1[0].hearts_high():
                moves.append(card)
    elif double(cards1):
        moves = _find_doubles(cards1, cards2)
    elif triple(cards1):
        moves = _find_triples(cards1, cards2)
    elif quad(cards1):
        moves = _find_quads(cards1, cards2)
    elif straight(cards1):
        moves = _find_straights(cards1, cards2)
    elif double-straight(cards1):
        pass

    return moves
