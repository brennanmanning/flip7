from dataclasses import dataclass
from typing import List, Union

from card import SpecialCard
from game import (
    GameState,
    player_draw,
    handle_stay,
    GamePhase,
    handle_special_card_targeting,
)
from player import check_for_card


@dataclass(frozen=True)
class TurnStartAction:
    pass


@dataclass(frozen=True)
class DrawAction(TurnStartAction):
    pass


@dataclass(frozen=True)
class StayAction(TurnStartAction):
    pass


@dataclass(frozen=True)
class PostDrawAction:
    pass


@dataclass(frozen=True)
class TargetPlayerAction(PostDrawAction):
    target_player_idx: int


def get_special_card_actions(gs: GameState) -> List[PostDrawAction]:
    if gs.pending_card is None:
        return []

    match gs.pending_card:
        case SpecialCard.FREEZE | SpecialCard.FLIP3:
            valid_targets = []
            for i, player in enumerate(gs.players):
                if not player.frozen_p:
                    valid_targets.append(TargetPlayerAction(i))
            return valid_targets
        case SpecialCard.CHANCE2:
            valid_targets = []
            for i, player in enumerate(gs.players):
                if not player.frozen_p and not check_for_card(
                    player, SpecialCard.CHANCE2
                ):
                    valid_targets.append(TargetPlayerAction(i))
            return valid_targets
        case _:
            return []


def get_legal_actions(gs: GameState) -> List[Union[TurnStartAction, PostDrawAction]]:
    match gs.phase:
        case GamePhase.TURNSTART:
            actions = [StayAction()]
            if not gs.players[gs.current_player_idx].frozen_p:
                actions.append(DrawAction())
            return actions
        case GamePhase.POSTDRAW:
            return get_special_card_actions(gs)


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
