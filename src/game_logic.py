import dataclasses
import random
from typing import List, Union

from game_state import GameState, GamePhase
import game_state as game
from card import Deck, SpecialCard, ModifierCard, NumberCard, count_number_cards
from player import freeze_player, add_card_hand, remove_card, check_for_card, empty_hand
from actions import (
    TurnStartAction,
    PostDrawAction,
    DrawAction,
    StayAction,
    TargetPlayerAction,
    get_legal_actions,
)


def refill_deck(gs: GameState):
    gs = dataclasses.replace(gs, deck=gs.discard_pile)
    gs = dataclasses.replace(gs, discard_pile=Deck(tuple()))
    return gs


def all_players_frozen_p(gs: GameState):
    return all(p.frozen_p for p in gs.players)


def get_input(actions: List[Union[TurnStartAction, PostDrawAction]]):
    idx = random.randrange(len(actions))
    return actions[idx]


def handle_stay(gs: GameState):
    p = gs.players[gs.current_player_idx]
    p = freeze_player(p)
    return game.update_players_single(gs, p, gs.current_player_idx)


def handle_special_card_targeting(gs: GameState, target_idx: int):
    pc = gs.pending_card
    match pc:
        case SpecialCard.FREEZE:
            p = gs.players[target_idx]
            p = freeze_player(p)
            gs = game.update_players_single(gs, p, target_idx)
        case SpecialCard.FLIP3:
            current_idx = gs.current_player_idx
            gs = game.update_current_player_idx(gs, target_idx)
            for _ in range(3):
                gs = player_draw(gs)
            gs = game.update_current_player_idx(gs, current_idx)
        case SpecialCard.CHANCE2:
            p = gs.players[target_idx]
            p = add_card_hand(p, SpecialCard.CHANCE2)
            gs = game.update_players_single(gs, p, target_idx)
        case _:
            pass
    return gs


def apply_action(
    gs: GameState, action: Union[TurnStartAction, PostDrawAction]
) -> GameState:
    match (gs.phase, action):
        case (GamePhase.TURNSTART, DrawAction()):
            return player_draw(gs)
        case (GamePhase.TURNSTART, StayAction()):
            return handle_stay(gs)
        case (GamePhase.POSTDRAW, TargetPlayerAction(target_idx)):
            return handle_special_card_targeting(gs, target_idx)
        case _:
            raise ValueError(f"Invalid action {action} for phase {gs.phase}")


def player_draw(gs: GameState) -> GameState:
    if not gs.round_active:
        return gs
    if len(gs.deck) == 0:
        gs = refill_deck(gs)
    gs = game.update_game_phase(gs, GamePhase.POSTDRAW)
    p = gs.players[gs.current_player_idx]
    if p.frozen_p:
        return gs
    card, gs = game.draw_card_deck(gs)
    match card:
        case SpecialCard.CHANCE2:
            if check_for_card(p, card):
                gs = game.update_pending_card(gs, card)
                legal_actions = get_legal_actions(gs)
                if len(legal_actions) == 0:
                    gs = game.add_card_discard(gs, card)
                else:
                    action = get_input(legal_actions)
                    gs = apply_action(gs, action)
            else:
                p = add_card_hand(p, card)
        case SpecialCard.FREEZE:
            gs = game.update_pending_card(gs, card)
            legal_actions = get_legal_actions(gs)
            action = get_input(legal_actions)
            gs = apply_action(gs, action)
        case SpecialCard.FLIP3:
            gs = game.update_pending_card(gs, card)
            legal_actions = get_legal_actions(gs)
            action = get_input(legal_actions)
            gs = apply_action(gs, action)
        case ModifierCard():
            p = add_card_hand(p, card)
        case NumberCard():
            if check_for_card(p, card):
                if check_for_card(p, SpecialCard.CHANCE2):
                    gs = game.add_card_discard(gs, card)
                    p = remove_card(p, SpecialCard.CHANCE2)
                    gs = game.add_card_discard(gs, SpecialCard.CHANCE2)
                else:
                    gs = game.add_card_discard(gs, card)
                    gs = game.add_card_discard(gs, p.hand)
                    p = empty_hand(p)
                    p = freeze_player(p)
            else:
                p = add_card_hand(p, card)
                nc = count_number_cards(p.hand)
                gs = game.update_round_active(gs, nc != 7)

    return game.update_players_single(gs, p, gs.current_player_idx)
