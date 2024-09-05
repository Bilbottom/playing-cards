"""
Define the cards and decks.

A deck in the traditional sense is a collection of 52 playing cards from
the French-suited, standard 52-card pack.

There are currently no Joker cards.
"""

from __future__ import annotations

import dataclasses
import enum
import functools
import itertools
import pathlib
import random
import tomllib
import typing
from typing import Any, Literal

Colour = Literal["black", "red"]

HERE = pathlib.Path(__file__).parent
SUITS: dict[str, dict[str, str]] = tomllib.loads(
    (HERE / "suits.toml").read_text(encoding="utf-8")
)
RANKS: dict[str, dict[str, str]] = tomllib.loads(
    (HERE / "ranks.toml").read_text(encoding="utf-8")
)


class Suit(enum.StrEnum):
    """
    A suit for a playing card.
    """

    CLUB = "club"
    SPADE = "spade"
    HEART = "heart"
    DIAMOND = "diamond"

    @functools.total_ordering
    def __lt__(self, other: Suit) -> bool:
        order = {
            Suit.CLUB: 0,
            Suit.DIAMOND: 1,
            Suit.HEART: 2,
            Suit.SPADE: 3,
        }
        return order[self] < order[other]

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return SUITS[self.value][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Suit:
        """
        Return a ``Rank`` from its corresponding character.

        :raises KeyError: If the key does not correspond to a valid suit.
        """
        for suit, properties in SUITS.items():
            if properties["id"] == _id:
                return cls(suit)

        raise KeyError(f"The key '{_id}' is not a valid suit")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the suit.
        """
        return self._get("id")

    @property
    def image(self) -> str:
        """
        The image corresponding to the suit.
        """
        return self._get("image")

    @property
    def colour(self) -> Colour:
        """
        The colour corresponding to the suit.
        """
        return self._get("colour")


class Rank(enum.IntEnum):
    """
    A rank for a playing card.

    Note that Ace is low in this implementation.
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @functools.total_ordering
    def __lt__(self, other: Rank) -> bool:
        return self.value < other.value

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return RANKS[str(self.value)][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Rank:
        """
        Return a ``Rank`` from its corresponding character.
        """
        for rank, properties in RANKS.items():
            if properties["id"] == _id:
                return cls(int(rank))

        raise KeyError(f"The key '{_id}' is not a valid rank")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the rank.
        """
        return self._get("id")


@typing.runtime_checkable
class ICard(typing.Protocol):
    """
    Interface for a playing card.
    """

    rank: Rank
    suit: Suit

    def __init__(self, rank: Rank, suit: Suit):
        pass  # pragma: no cover

    @classmethod
    def from_id(cls, _key: str, /) -> ICard:
        """
        Return a card corresponding to the string.
        """
        pass  # pragma: no cover

    @property
    def face(self) -> str:
        """
        The face of the card.
        """
        pass  # pragma: no cover

    @property
    def value(self) -> int:
        """
        The value of the card.
        """
        pass  # pragma: no cover

    @property
    def colour(self) -> Colour:
        """
        The colour of the card.
        """
        pass  # pragma: no cover


@dataclasses.dataclass
class Card:
    """
    A playing card from the French-suited, standard 52-card pack.
    """

    rank: Rank
    suit: Suit

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank.id + self.suit.id

    @classmethod
    def from_id(cls, _id: str, /) -> Card:
        """
        Return a ``Card`` corresponding to the string.
        """
        if len(_id) != 2:  # noqa: PLR2004
            raise KeyError(f"The key, {_id}, should be 2 characters")
        return cls(Rank.from_id(_id[0]), Suit.from_id(_id[1]))

    @property
    def face(self) -> str:
        """
        The face of the card.

        This shows the rank and then the image of the suit.
        """
        return self.rank.id + self.suit.image

    @property
    def value(self) -> int:
        """
        The value of the card.
        """
        return self.rank.value

    @property
    def colour(self) -> Colour:
        """
        The colour of the card.
        """
        return self.suit.colour


class Deck:
    """
    A set of 52-card French-suited playing cards.
    """

    cards: list[ICard]

    def __init__(self, card_type: type[ICard] = Card):
        """
        Return a ``Deck`` with 52 cards.
        """
        self._card_type = card_type
        self.cards = []
        self.reset()

    def __repr__(self):
        return "Deck()"

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position: int):
        return self.cards[position]

    def reset(self) -> None:
        """
        Reset the deck to have all cards in it, then shuffle it.
        """
        rank: Rank  # noqa: F842
        suit: Suit  # noqa: F842
        self.cards = [
            self._card_type(rank, suit)
            for rank, suit in itertools.product(Rank, Suit)
        ]

        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffle the deck.
        """
        random.shuffle(self.cards)

    def take_card(self, _id: str | None = None, /) -> ICard:
        """
        Return the top card from the deck.

        :param _id: The key of the card to take instead of the top card.

        :return: The card taken from the deck.

        :raises IndexError: If the deck is empty.
        """
        return self._take_card_by_id(_id) if _id else self.cards.pop()

    def _take_card_by_id(self, _id: str) -> ICard:
        """
        Pop the card ``id_`` from the deck.

        :param _id: The ID of the card to take.

        :return: The card taken from the deck.

        :raises KeyError: If the card has already been removed from the deck.
        """
        for i, card in enumerate(self.cards):
            if str(card) == _id:
                return self.cards.pop(i)

        raise KeyError(f"The card with key '{_id}' is not in the deck")


class Decks(Deck):
    """
    A set of multiple decks of cards.
    """

    def __init__(self, n: int, card_type: type[ICard] = Card):
        """
        Return a set of ``n`` decks of cards.
        """
        self.number_of_decks = n
        super().__init__(card_type)  # type: ignore

    def reset(self) -> None:
        """
        Reset the decks to have all cards in them, then shuffle them.
        """
        rank: Rank  # noqa: F842
        suit: Suit  # noqa: F842
        self.cards = []
        for _ in range(self.number_of_decks):
            self.cards.extend(
                self._card_type(rank, suit)
                for rank, suit in itertools.product(Rank, Suit)
            )

        self.shuffle()
