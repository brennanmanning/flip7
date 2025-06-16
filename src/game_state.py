from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Tuple, Optional, Union

from player import Player, new_player
from card import Deck, Card, add_cards, draw_card, create_deck


class GamePhase(Enum):
    TURNSTART, POSTDRAW = range(2)


@dataclass
class GameState:
    players: Tuple[Player, ...]
    deck: Deck
    phase: GamePhase = GamePhase.TURNSTART
    discard_pile: Deck = Deck(tuple())
    round: int = 0
    current_player_idx: int = 0
    round_active: bool = True
    target_score: int = 200
    pending_card: Optional[Card] = None


def update_players(gs: GameState, new_players: Tuple[Player]):
    return dataclasses.replace(gs, players=new_players)


def update_players_single(gs: GameState, new_player: Player, idx: int):
    new_players = tuple(new_player if i == idx else x for i, x in enumerate(gs.players))
    return dataclasses.replace(gs, players=new_players)


def add_card_discard(gs: GameState, card: Union[Card, Deck]) -> GameState:
    return dataclasses.replace(gs, discard_pile=add_cards(gs.discard_pile, card))


def update_pending_card(gs: GameState, card: Card):
    return dataclasses.replace(gs, pending_card=card)


def update_game_phase(gs: GameState, gp: GamePhase):
    return dataclasses.replace(gs, phase=gp)


def update_round_active(gs: GameState, active_p: bool):
    return dataclasses.replace(gs, round_active=active_p)


def update_current_player_idx(gs: GameState, idx: int):
    return dataclasses.replace(gs, current_player_idx=idx)


def draw_card_deck(gs: GameState) -> Tuple[Card, GameState]:
    card, deck = draw_card(gs.deck)
    return card, dataclasses.replace(gs, deck=deck)


def new_game(n_players: int) -> GameState:
    deck = create_deck()
    players = [new_player() for _ in range(n_players)]
    return GameState(tuple(players), deck)
