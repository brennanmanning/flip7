from card import Deck, create_deck, draw_card, add_cards, value_hand

# def turn(player: Player, gs: GameState):
#     card, new_deck = draw_card(gs.deck)
#     match card:
#         case SpecialCard.CHANCE2:
#             if check_duplicates(player, card):
#                 print("give other player card")
#             else:
#                 player = add_card_hand(player, card)
#                 return None
#         case SpecialCard.FREEZE:
#             print("give other player card or yourself")
#         case SpecialCard.FLIP3:
#             print("give other player card or yourself")
#         case SpecialCard.X2:
#             player = add_card_hand(player, card)
#             return None
#         case AdderCard():
#             player = add_card_hand(player, card)
#             return None
#         case NumberCard():
#             if check_duplicates(player, card):
#                 if check_second_chance(player):
#                     gs = add_card_discard(gs, card)
#
#                 gs = add_card_discard(gs, player.hand)
#                 player = empty_hand(player)
#                 player = freeze_player(player)
#                 return None
#             else:
#                 player = add_card_hand(player, card)
#


def main():
    # TODO Think about how to deal with deck with cards in play
    deck = create_deck()
    hand = Deck(tuple())
    for _ in range(5):
        card, deck = draw_card(deck)
        if card in deck:
            print("Hey, we got a dupe here!")
            hand = Deck(tuple())
        else:
            hand = add_cards(hand, card)
    print(f"New deck size: {len(deck)}")
    print(f"Value of Hand: {value_hand(hand)}")
    print(hand)


if __name__ == "__main__":
    main()
