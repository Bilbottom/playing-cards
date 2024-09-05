"""
Test the ``playing_cards.Decks`` class.
"""

import pytest

from playing_cards import Card, Colour, Decks, Rank, Suit


def test__decks__can_be_initialised():
    """
    Test that decks can be initialised.
    """
    deck_1, deck_2, deck_3 = Decks(1), Decks(2), Decks(3)
    assert len(deck_1) == 52
    assert len(deck_2) == 104
    assert len(deck_3) == 156


def test__decks__can_be_initialised_with_default_card_type():
    """
    Test that decks can be initialised.
    """
    deck = Decks(2, card_type=Card)
    assert len(deck) == 104
    assert type(deck[0]) is Card


def test__decks__can_be_initialised_with_custom_card_type():
    """
    Test that decks can be initialised.
    """

    class CustomCard:
        rank: Rank
        suit: Suit

        def __init__(self, rank: Rank, suit: Suit):
            self.rank = rank
            self.suit = suit

        @classmethod
        def from_id(cls, _key: str, /):
            """
            Return a card corresponding to the string.
            """
            return cls(Rank("A"), Suit("S"))  # pragma: no cover

        @property
        def face(self) -> str:
            """
            The face of the card.
            """
            return "AS"

        @property
        def value(self) -> int:
            """
            The value of the card.
            """
            return 1

        @property
        def colour(self) -> Colour:
            """
            The colour of the card.
            """
            return "red"

    deck = Decks(2, card_type=CustomCard)
    assert len(deck) == 104

    card = deck.take_card()
    assert type(card) is CustomCard
    assert card.face == "AS"
    assert card.value == 1
    assert card.colour == "red"


def test__decks__taking_a_card_makes_the_deck_smaller():
    """
    Test that taking a card from the deck makes it smaller.
    """
    deck = Decks(2)
    card = deck.take_card()
    assert len(deck) == 103
    assert type(card) is Card
    assert card in deck


def test__decks__card_cannot_be_taken_from_empty_deck():
    """
    Test that taking a card from an empty deck raises an error.
    """
    deck = Decks(2)
    [deck.take_card() for _ in range(104)]

    with pytest.raises(IndexError):
        deck.take_card()


@pytest.mark.parametrize(
    "id_, card",
    [
        ("AC", Card(Rank.ACE, Suit.CLUB)),
        ("2S", Card(Rank.TWO, Suit.SPADE)),
        ("TH", Card(Rank.TEN, Suit.HEART)),
        ("KD", Card(Rank.KING, Suit.DIAMOND)),
    ],
)
def test__decks__cards_can_be_taken_by_id(id_: str, card: Card):
    """
    Test that cards can be taken by ID.
    """
    deck = Decks(2)
    taken_card = deck.take_card(id_)
    assert len(deck) == 103
    assert taken_card == card
    assert taken_card in deck


def test__decks__multiple_cards_can_be_taken_by_id():
    """
    Test that cards can be taken multiple times by their ID.
    """
    key = "AS"
    card = Card.from_id(key)
    deck = Decks(2)

    taken_card_1 = deck.take_card(key)
    assert len(deck) == 103
    assert taken_card_1 == card
    assert taken_card_1 in deck

    taken_card_2 = deck.take_card(key)
    assert len(deck) == 102
    assert taken_card_2 == card
    assert taken_card_2 not in deck


def test__decks__card_cannot_be_taken_by_id_if_it_is_not_in_the_deck():
    """
    Test that cards cannot be taken by ID if they are not in the deck.
    """
    key = "AS"
    deck = Decks(2)

    deck.take_card(key)
    deck.take_card(key)
    with pytest.raises(KeyError):
        deck.take_card(key)


def test__decks__can_be_reset():
    """
    Test that decks can be reset.
    """
    deck = Decks(2)
    [deck.take_card() for _ in range(10)]
    assert len(deck) == 94

    deck.reset()
    assert len(deck) == 104
