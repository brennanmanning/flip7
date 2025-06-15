from dataclasses import dataclass
import dataclasses
from enum import Enum
import random
from typing import List, Optional, Union, Tuple

from actions import PostDrawAction, TurnStartAction, apply_action, get_legal_actions
from card import (
    Deck,
    SpecialCard,
    add_cards,
    Card,
    create_deck,
    draw_card,
    ModifierCard,
    NumberCard,
    count_number_cards,
)
from player import Player, add_card_hand, freeze_player
import player as player
from utils import bounded_add


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
    players = [player.new_player() for _ in range(n_players)]
    return GameState(tuple(players), deck)


def all_players_frozen_p(gs: GameState):
    return all(p.frozen_p for p in gs.players)


def get_input(actions: List[Union[TurnStartAction, PostDrawAction]]):
    idx = random.randrange(len(actions))
    return actions[idx]


def match(n_players: int = 2):
    winner = n_players + 1
    gs = new_game(n_players)
    for _ in range(200):
        gs = round(gs)
        scores = [p.score for p in gs.players]
        if max(scores) > gs.target_score:
            winner = scores.index(max(scores))
            break
        gs = dataclasses.replace(gs, round=gs.round + 1)
    return winner


def round(gs: GameState) -> GameState:
    n_players = len(gs.players)
    for _ in range(n_players):
        current_idx = gs.current_player_idx
        gs = turn(gs)
        new_idx = bounded_add(current_idx, n_players)
        gs = update_current_player_idx(gs, new_idx)
        gs = update_round_active(gs, all_players_frozen_p(gs))
        if not gs.round_active:
            break
    new_players = []
    for p in gs.players:
        p = player.update_score(p)
        p = player.empty_hand(p)
        new_players.append(p)
    gs = update_players(gs, tuple(new_players))
    return gs


def turn(gs: GameState) -> GameState:
    gs = update_game_phase(gs, GamePhase.TURNSTART)
    legal_actions = get_legal_actions(gs)
    if len(legal_actions) > 1:
        action = get_input(legal_actions)
    else:
        action = legal_actions[0]
    gs = apply_action(gs, action)
    return gs


def handle_stay(gs: GameState):
    p = gs.players[gs.current_player_idx]
    p = freeze_player(p)
    return update_players_single(gs, p, gs.current_player_idx)


def handle_special_card_targeting(gs: GameState, target_idx: int):
    pc = gs.pending_card
    match pc:
        case SpecialCard.FREEZE:
            p = gs.players[target_idx]
            p = freeze_player(p)
            gs = update_players_single(gs, p, target_idx)
        case SpecialCard.FLIP3:
            current_idx = gs.current_player_idx
            gs = update_current_player_idx(gs, target_idx)
            for _ in range(3):
                gs = player_draw(gs)
            gs = update_current_player_idx(gs, current_idx)
        case SpecialCard.CHANCE2:
            p = gs.players[target_idx]
            p = add_card_hand(p, SpecialCard.CHANCE2)
            gs = update_players_single(gs, p, target_idx)
        case _:
            pass
    return gs


def refill_deck(gs: GameState):
    gs = dataclasses.replace(gs, deck=gs.discard_pile)
    gs = dataclasses.replace(gs, discard_pile=Deck(tuple()))
    return gs


def player_draw(gs: GameState) -> GameState:
    if not gs.round_active:
        return gs
    gs = update_game_phase(gs, GamePhase.POSTDRAW)
    p = gs.players[gs.current_player_idx]
    if p.frozen_p:
        return gs
    card, gs = draw_card_deck(gs)
    if len(gs.deck) == 0:
        gs = refill_deck(gs)
    match card:
        case SpecialCard.CHANCE2:
            if player.check_for_card(p, card):
                gs = update_pending_card(gs, card)
                legal_actions = get_legal_actions(gs)
                if len(legal_actions) == 0:
                    gs = add_card_discard(gs, card)
                else:
                    action = get_input(legal_actions)
                    gs = apply_action(gs, action)
            else:
                p = player.add_card_hand(p, card)
        case SpecialCard.FREEZE:
            gs = update_pending_card(gs, card)
            legal_actions = get_legal_actions(gs)
            action = get_input(legal_actions)
            gs = apply_action(gs, action)
        case SpecialCard.FLIP3:
            gs = update_pending_card(gs, card)
            legal_actions = get_legal_actions(gs)
            action = get_input(legal_actions)
            gs = apply_action(gs, action)
        case ModifierCard():
            p = player.add_card_hand(p, card)
        case NumberCard():
            if player.check_for_card(p, card):
                if player.check_for_card(p, SpecialCard.CHANCE2):
                    gs = add_card_discard(gs, card)
                    p = player.remove_card(p, SpecialCard.CHANCE2)
                    gs = add_card_discard(gs, SpecialCard.CHANCE2)
                else:
                    gs = add_card_discard(gs, card)
                    gs = add_card_discard(gs, p.hand)
                    p = player.empty_hand(p)
                    p = player.freeze_player(p)
            else:
                p = player.add_card_hand(p, card)
                nc = count_number_cards(p.hand)
                gs = update_round_active(gs, nc == 7)

    return update_players_single(gs, p, gs.current_player_idx)
