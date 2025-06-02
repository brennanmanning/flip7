from dataclasses import dataclass
from functools import reduce
from main import NumberCard
from src.card import Card, ModifierCard, SpecialCard
from typing import Tuple


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
