import dataclasses

from actions import get_legal_actions
from game_state import GameState, GamePhase, new_game
import game_state as game
from game_logic import all_players_frozen_p, apply_action, get_input
from player import empty_hand, unfreeze_player, update_score
from utils import bounded_add


def turn(gs: GameState) -> GameState:
    gs = game.update_game_phase(gs, GamePhase.TURNSTART)
    legal_actions = get_legal_actions(gs)
    if len(legal_actions) > 1:
        action = get_input(legal_actions)
    else:
        action = legal_actions[0]
    gs = apply_action(gs, action)
    return gs


def round(gs: GameState) -> GameState:
    n_players = len(gs.players)
    for _ in range(n_players):
        current_idx = gs.current_player_idx
        gs = turn(gs)
        new_idx = bounded_add(current_idx, n_players)
        gs = game.update_current_player_idx(gs, new_idx)
        gs = game.update_round_active(gs, not all_players_frozen_p(gs))
        if not gs.round_active:
            break
    new_players = []
    for p in gs.players:
        p = update_score(p)
        p = empty_hand(p)
        p = unfreeze_player(p)
        new_players.append(p)
    gs = game.update_players(gs, tuple(new_players))
    return gs


def start_match(n_players: int = 2):
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
