from dataclasses import dataclass
from typing import List, Union

from game_state import GameState, GamePhase
from card import SpecialCard
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
            for i, p in enumerate(gs.players):
                if not p.frozen_p:
                    valid_targets.append(TargetPlayerAction(i))
            return valid_targets
        case SpecialCard.CHANCE2:
            valid_targets = []
            for i, p in enumerate(gs.players):
                if not p.frozen_p and not check_for_card(p, SpecialCard.CHANCE2):
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
