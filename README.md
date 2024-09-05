<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![tests](https://github.com/Bilbottom/playing-cards/actions/workflows/tests.yaml/badge.svg)](https://github.com/Bilbottom/playing-cards/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
[![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/playing-cards)](https://shields.io/badges/git-hub-last-commit)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/playing-cards/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/playing-cards/main)
[![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)

</div>

---

# Playing Cards 🃏

Playing cards from the French-suited, standard 52-card pack.

## Installation ⬇️

This package is currently only available from GitHub:

```
pip install git+https://github.com/Bilbottom/playing-cards@v0.0.1
```

## Usage 📖

This library provides classes to represent playing cards and decks of cards.

Import the package and start using the classes. Here's an example of a simple game of _Red or Black_:

```python
import playing_cards


def ask(choices: list[str]) -> str:
    """Ask a question and return the user's choice."""
    question = f"{', '.join(choices[:-1])} or {choices[-1]}? "
    while (choice := input(question).lower()) not in choices:
        pass

    return choice


def print_cards(cards: list[playing_cards.Card]) -> None:
    """Print the faces of the cards in the list."""
    print(f"[{', '.join(card.face for card in cards)}]")


def red_or_black() -> None:
    """Play a game of Red or Black."""
    deck = playing_cards.Deck()
    cards: list[playing_cards.Card] = []

    ###  red or black
    colour_choice = ask(["red", "black"])
    cards.append(deck.take_card()), print_cards(cards)
    if cards[-1].colour != colour_choice:
        print("Wrong colour. You lose!")
        return

    ###  higher or lower (ties lose)
    hl_choice = ask(["higher", "lower"])
    cards.append(deck.take_card()), print_cards(cards)
    is_higher = cards[-1].rank > cards[-2].rank
    is_lower = cards[-1].rank < cards[-2].rank
    if not (
        (hl_choice == "higher" and is_higher)
        or (hl_choice == "lower" and is_lower)
    ):
        print("Wrong direction. You lose!")
        return

    ###  inside or outside (only inside is inclusive)
    io_choice = ask(["inside", "outside"])
    cards.append(deck.take_card()), print_cards(cards)
    rank_min, rank_max = sorted([cards[-3].rank, cards[-2].rank])
    is_inside = rank_min <= cards[-1].rank <= rank_max
    if not (
        (io_choice == "inside" and is_inside)
        or (io_choice == "outside" and not is_inside)
    ):
        print("Wrong range. You lose!")
        return

    ###  suit
    suit_choice = ask(list(playing_cards.Suit))
    cards.append(deck.take_card()), print_cards(cards)
    if cards[-1].suit != suit_choice:
        print("Wrong suit. You lose!")
        return

    print("You win!")


if __name__ == "__main__":
    red_or_black()
```

## Modifying the Deck 🃏

The `Deck` and `Decks` classes can use custom `Card` classes via their `card_type` parameter. This can be handy for customising cards for specific games.

```python
import playing_cards


class CardWithAceHigh(playing_cards.Card):
    """A card with the Ace ranked higher than the King."""

    @property
    def value(self) -> int:
        """Return the value of the card."""
        return self.rank.value if self.rank.value != 1 else 14


def main():
    """Create a deck of cards with the Ace ranked higher than the King."""
    deck = playing_cards.Deck(card_type=CardWithAceHigh)
    ace = deck.take_card("AS")
    king = deck.take_card("KH")
    print(ace.value > king.value)  # True
```

## Contributing 🤝

Install poetry and pre-commit:

```bash
poetry install --sync --with dev,test
pre-commit install --install-hooks
```
