import random
from functools import reduce
import dataclasses
from dataclasses import dataclass
from typing import List, Tuple, Union, Sequence
from enum import Enum


def list_tuple(data: Tuple, idx: int) -> Tuple:
    return data[:idx] + data[idx + 1 :]


@dataclass(frozen=True)
class NumberCard:
    value: int


class SpecialCard(Enum):
    X2, FREEZE, CHANCE2, FLIP3 = range(4)


class AdderCard(Enum):
    TWO, FOUR, SIX, EIGHT, TEN = 2, 4, 6, 8, 10


Card = Union[NumberCard, SpecialCard, AdderCard]


@dataclass(frozen=True)
class Deck:
    cards: Tuple[Card, ...]

    def __len__(self):
        return len(self.cards)

    def __contains__(self, card):
        return card in self.cards

    def __iter__(self):
        for card in self.cards:
            yield card


def pop_deck(deck: Deck, idx: int = 1) -> Tuple[Card, Deck]:
    return deck.cards[idx], Deck(list_tuple(deck.cards, idx))


def add_cards(deck: Deck, cards: Union[Sequence[Card], Card, Deck]) -> Deck:
    if isinstance(cards, (list, tuple)):
        return Deck(deck.cards + tuple(cards))
    elif isinstance(cards, Deck):
        return Deck(deck.cards + cards.cards)
    elif (type(cards) is NumberCard) | (type(cards) is SpecialCard):
        return Deck(deck.cards + (cards,))
    else:
        raise ValueError(f"cards must be a list of Card or a Card! Got {type(cards)}")


def create_deck() -> Deck:
    numbers = [0] + reduce(lambda x, y: x + y, [[i] * i for i in range(1, 13)])
    numbers = [NumberCard(x) for x in numbers]
    special = (
        [SpecialCard.X2]
        + [SpecialCard.FREEZE] * 3
        + [SpecialCard.CHANCE2] * 3
        + [SpecialCard.FLIP3] * 3
    )
    adders = [x for x in AdderCard]
    cards = numbers + special + adders
    return Deck(tuple(cards))


def draw_card(deck: Deck) -> Tuple[Card, Deck]:
    idx = random.randrange(len(deck))
    card, deck = pop_deck(deck, idx)
    return card, deck


def value(hand: Deck) -> int:
    if SpecialCard.X2 in hand:
        mult = 2
    else:
        mult = 1

    value = 0
    for card in hand:
        match card:
            case NumberCard():
                value += card.value
            case AdderCard():
                value += card.value
    return mult * value


@dataclass
class Player:
    hand: Deck
    cumulative_score: int
    is_frozen: bool = False


@dataclass
class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: Deck
    current_player_idx: int
    round_active: bool
    target_score: int = 200


def new_player() -> Player:
    return Player(Deck(tuple()), 0)


def freeze_player(player: Player) -> Player:
    return dataclasses.replace(player, frozen=True)


def check_duplicates(player: Player, card: Card):
    if card in player.hand:
        return True
    else:
        return False


def check_second_chance(player: Player):
    if SpecialCard.CHANCE2 in player.hand:
        return True
    else:
        return False


def add_card_hand(player: Player, card: Card):
    return dataclasses.replace(player, hand=add_cards(player.hand, card))


def add_card_discard(gs: GameState, card: Union[Card, Deck]):
    return dataclasses.replace(gs, discard_pile=add_cards(gs.discard_pile, card))


def empty_hand(player: Player):
    return dataclasses.replace(player, hand=Deck(tuple()))


# def turn(player: Player, gs: GameState):
#     card, new_deck = draw_card(gs.deck)
#     match card:
#         case SpecialCard.CHANCE2:
#             if check_duplicates(player, card):
#                 print("give other player card")
#             else:
#                 player = add_card_hand(player, card)
#                 return None
#         case SpecialCard.FREEZE:
#             print("give other player card or yourself")
#         case SpecialCard.FLIP3:
#             print("give other player card or yourself")
#         case SpecialCard.X2:
#             player = add_card_hand(player, card)
#             return None
#         case AdderCard():
#             player = add_card_hand(player, card)
#             return None
#         case NumberCard():
#             if check_duplicates(player, card):
#                 if check_second_chance(player):
#                     gs = add_card_discard(gs, card)
#
#                 gs = add_card_discard(gs, player.hand)
#                 player = empty_hand(player)
#                 player = freeze_player(player)
#                 return None
#             else:
#                 player = add_card_hand(player, card)
#


def main():
    # TODO Think about how to deal with deck with cards in play
    deck = create_deck()
    hand = Deck(tuple())
    for _ in range(5):
        card, deck = draw_card(deck)
        if card in deck:
            print("Hey, we got a dupe here!")
            hand = Deck(tuple())
        else:
            hand = add_cards(hand, card)
    print(f"New deck size: {len(deck)}")
    print(f"Value of Hand: {value(hand)}")
    print(hand)


if __name__ == "__main__":
    main()
