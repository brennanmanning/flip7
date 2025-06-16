from enum import Enum
from dataclasses import dataclass


class GamePhase(Enum):
    TURNSTART, POSTDRAW = range(2)


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
