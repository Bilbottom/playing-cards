"""
Test the ``playing_cards.Card`` class.
"""

import itertools

import pytest

from playing_cards import Card, Rank, Suit


def _ranks_and_suits() -> list[tuple[Rank, Suit]]:
    """
    Return all possible combinations of ranks and suits.
    """
    yield from itertools.product(Rank, Suit)


def test__card__can_be_initialised():
    """
    Test that cards can be initialised.
    """
    for rank, suit in _ranks_and_suits():
        card = Card(rank, suit)
        assert card.rank == rank
        assert card.suit == suit
        assert str(card) == rank.id + suit.id
        assert repr(card) == f"Card({rank=}, {suit=})"


def test__card__can_be_initialised_from_an_id():
    """
    Test that cards can be initialised from an ID.
    """
    for rank, suit in _ranks_and_suits():
        card = Card.from_id(rank.id + suit.id)
        assert card.rank == rank
        assert card.suit == suit


@pytest.mark.parametrize(
    "invalid_id",
    ["A", "1", "X", "A0", "X1", "X0"],
)
def test__card__cannot_be_initialised_from_an_invalid_id(invalid_id: str):
    """
    Test that cards cannot be initialised from an invalid ID.
    """
    with pytest.raises(KeyError):
        Card.from_id(invalid_id)


def test__card__face_is_the_rank_id_with_the_suit_image():
    """
    Test that a card's face is the rank ID with the suit image.
    """
    for rank, suit in _ranks_and_suits():
        card = Card(rank, suit)
        # This reimplements the `face` logic. Can we test this better?
        assert card.face == (rank.id + suit.image)


def test__card__value_is_the_rank_value():
    """
    Test that a card's value is the rank value.
    """
    for rank, suit in _ranks_and_suits():
        card = Card(rank, suit)
        assert card.value == rank.value


def test__card__colour_is_the_suit_colour():
    """
    Test that a card's colour is the suit colour.
    """
    for rank, suit in _ranks_and_suits():
        card = Card(rank, suit)
        assert card.colour == suit.colour
