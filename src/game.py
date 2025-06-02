from dataclasses import dataclass
import dataclasses
from typing import List, Union

from card import Deck, add_cards, Card
from player import Player


@dataclass
class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: Deck
    current_player_idx: int
    round_active: bool
    target_score: int = 200


def add_card_discard(gs: GameState, card: Union[Card, Deck]):
    return dataclasses.replace(gs, discard_pile=add_cards(gs.discard_pile, card))
