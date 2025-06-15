from dataclasses import dataclass
import dataclasses

from card import Card, Deck, add_cards, pop_deck, card_index, value_hand


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


def add_card_hand(player: Player, card: Card) -> Player:
    return dataclasses.replace(player, hand=add_cards(player.hand, card))


def empty_hand(player: Player) -> Player:
    return dataclasses.replace(player, hand=Deck(tuple()))


def remove_card(player: Player, card: Card) -> Player:
    card_idx = card_index(player.hand, card)
    _, new_hand = pop_deck(player.hand, card_idx)
    return dataclasses.replace(player, hand=new_hand)


def update_score(player: Player):
    hand_value = value_hand(player.hand)
    return dataclasses.replace(player, score=hand_value + player.score)
