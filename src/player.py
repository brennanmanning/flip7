from dataclasses import dataclass
import dataclasses

from card import Card, Deck, add_cards


@dataclass(frozen=True)
class Player:
    hand: Deck
    score: int
    frozen_p: bool = False


def new_player() -> Player:
    return Player(Deck(tuple()), 0)


def freeze_player(player: Player) -> Player:
    return dataclasses.replace(player, frozen_p=True)


def check_for_card(player: Player, card: Card) -> bool:
    return card in player.hand


def add_card_hand(player: Player, card: Card):
    return dataclasses.replace(player, hand=add_cards(player.hand, card))


def empty_hand(player: Player):
    return dataclasses.replace(player, hand=Deck(tuple()))
