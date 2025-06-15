from dataclasses import dataclass
import random
from functools import reduce
from enum import Enum
from typing import Union, Tuple, Sequence
from utils import pop_tuple


@dataclass(frozen=True)
class NumberCard:
    value: int


class SpecialCard(Enum):
    FREEZE, CHANCE2, FLIP3 = range(3)


class ModifierCard(Enum):
    X2, TWO, FOUR, SIX, EIGHT, TEN = 0, 2, 4, 6, 8, 10


Card = Union[NumberCard, SpecialCard, ModifierCard]


@dataclass(frozen=True)
class Deck:
    cards: Tuple[Card, ...]

    def __len__(self):
        return len(self.cards)

    def __contains__(self, card: Card):
        return card in self.cards

    def __iter__(self):
        for card in self.cards:
            yield card


def create_deck() -> Deck:
    numbers = [0] + reduce(lambda x, y: x + y, [[i] * i for i in range(1, 13)])
    numbers = [NumberCard(x) for x in numbers]
    special = reduce(lambda x, y: x + y, [[z] * 3 for z in SpecialCard])
    modifiers = [x for x in ModifierCard]
    cards = numbers + special + modifiers
    return Deck(tuple(cards))


def pop_deck(deck: Deck, idx: int) -> Tuple[Card, Deck]:
    return deck.cards[idx], Deck(pop_tuple(deck.cards, idx))


def add_cards(deck: Deck, cards: Union[Sequence[Card], Card, Deck]) -> Deck:
    if isinstance(cards, (list, tuple)):
        return Deck(deck.cards + tuple(cards))
    elif isinstance(cards, Deck):
        return Deck(deck.cards + cards.cards)
    elif isinstance(cards, Card):
        return Deck(deck.cards + (cards,))
    else:
        raise ValueError(
            f"cards must be a list of Card, a Card, or a Deck of Cards! Got {type(cards)}"
        )


def count_number_cards(hand: Deck) -> int:
    number_cards = [x for x in hand if isinstance(x, NumberCard)]
    return len(number_cards)


def value_hand(hand: Deck) -> int:
    if ModifierCard.X2 in hand:
        mult = 2
    else:
        mult = 1

    value = 0
    for card in hand:
        match card:
            case NumberCard():
                value += card.value
            case ModifierCard():
                value += card.value
    if count_number_cards(hand) == 7:
        value += 15
    return mult * value


def draw_card(deck: Deck) -> Tuple[Card, Deck]:
    idx = random.randrange(len(deck))
    card, deck = pop_deck(deck, idx)
    return card, deck


def card_index(deck: Deck, card: Card):
    if card not in deck:
        raise ValueError("Card {card} not found in deck!")
    return deck.cards.index(card)
