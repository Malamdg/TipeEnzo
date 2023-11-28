import random as rd
from enum import *


class Card:
    def __init__(self):
        return


class Deck:
    def __init__(self, cards: list):
        self.cards = cards

    def shuffle(self):
        # shuffle algorithm
        rd.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()

    def add_card(self, card: Card):
        self.cards.append(card)

    def merge_decks(self, deck):
        for i in range(0, len(deck.cards)):
            self.add_card(deck.draw())


class TrainColor(Enum):
    NONE = 0
    RED = 12
    BLUE = 12
    GREEN = 12
    YELLOW = 12
    ROSE = 12
    WHITE = 12
    BLACK = 12
    JOKER = 14


class TrainCard(Card):
    def __init__(self, color: TrainColor):
        super().__init__()
        self.color = color


class ObjectiveCard(Card):
    def __init__(self, start_city, destination_city, points):
        super().__init__()
        self.start = start_city
        self.destination = destination_city
        self.points = points


class ObjectiveCardsDeck(Deck):
    def __init__(self):
        super().__init__([])


class TrainCardsDeck(Deck):
    def __init__(self):
        super().__init__([])


class PlayerColors(Enum):
    def _generate_next_value_(name, start, count, last_values):
        ...
        return name.lower()
    RED = auto()
    BLUE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLACK = auto()

