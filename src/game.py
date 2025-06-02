from dataclasses import dataclass
import dataclasses
from typing import List, Union

from card import Deck, add_cards, Card, create_deck
from player import Player, new_player


@dataclass
class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: Deck = Deck(tuple())
    current_player_idx: int = 0
    round_active: bool = True
    target_score: int = 200


def add_card_discard(gs: GameState, card: Union[Card, Deck]) -> GameState:
    return dataclasses.replace(gs, discard_pile=add_cards(gs.discard_pile, card))


def new_game(n_players: int = 2) -> GameState:
    deck = create_deck()
    players = [new_player() for _ in range(n_players)]
    return GameState(players, deck)
