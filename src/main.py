from card import Deck, create_deck, draw_card, add_cards, value_hand


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
