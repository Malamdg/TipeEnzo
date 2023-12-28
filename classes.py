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
    BLACK = "black", 12
    BLUE = "blue", 12
    GREEN = "green", 12
    JOKER = "joker", 14
    ORANGE = "orange", 12
    PINK = "pink", 12
    RED = "red", 12
    YELLOW = "yellow", 12
    WHITE = "white", 12


class TrainCard(Card):
    def __init__(self, color: TrainColor):
        super().__init__()
        self.color = color

    def __str__(self):
        return self.color.value[0]


class ObjectiveCard(Card):
    def __init__(self, start_city, destination_city, points):
        super().__init__()
        self.start = start_city
        self.destination = destination_city
        self.points = points


class CityEnum(Enum):
    ATLANTA = "Atlanta"
    BOSTON = "Boston"
    CALGARY = "Calgary"
    CHICAGO = "Chicago"
    DALLAS = "Dallas"
    DENVER = "Denver"
    DULUTH = "Duluth"
    EL_PASO = "El Paso"
    HELENA = "Helena"
    HOUSTON = "Houston"
    KANSAS_CITY = "Kansas City"
    LITTLE_ROCK = "Little Rock"
    LOS_ANGELES = "Los Angeles"
    MIAMI = "Miami"
    MONTREAL = "Montréal"
    NASHVILLE = "Nashville"
    NEW_ORLEANS = "New Orleans"
    NEW_YORK = "New York"
    OKLAHOMA_CITY = "Oklahoma City"
    PHOENIX = "Phoenix"
    PITTSBURGH = "Pittsburgh"
    PORTLAND = "Portland"
    SALT_LAKE_CITY = "Salt Lake City"
    SAN_FRANCISCO = "San Fransisco"
    SANTA_FE = "Santa Fe"
    SAULT_STE_MARIE = "Sault Ste. Marie"
    SEATTLE = "Seattle"
    TORONTO = "Toronto"
    VANCOUVER = "Vancouver"
    WINNIPEG = "Winnipeg"


class ObjectiveCardsDeck(Deck):
    def __init__(self):
        super().__init__(
            [
                ObjectiveCard(CityEnum.HELENA, CityEnum.LOS_ANGELES, 8),
                ObjectiveCard(CityEnum.SAULT_STE_MARIE, CityEnum.NASHVILLE, 8),
                ObjectiveCard(CityEnum.TORONTO, CityEnum.MIAMI, 10),
                ObjectiveCard(CityEnum.CHICAGO, CityEnum.SANTA_FE, 9),
                ObjectiveCard(CityEnum.KANSAS_CITY, CityEnum.HOUSTON, 5),
                ObjectiveCard(CityEnum.NEW_YORK, CityEnum.ATLANTA, 6),
                ObjectiveCard(CityEnum.WINNIPEG, CityEnum.LITTLE_ROCK, 11),
                ObjectiveCard(CityEnum.LOS_ANGELES, CityEnum.NEW_YORK, 21),
                ObjectiveCard(CityEnum.DENVER, CityEnum.PITTSBURGH, 11),
                ObjectiveCard(CityEnum.DENVER, CityEnum.EL_PASO, 4),
                ObjectiveCard(CityEnum.PORTLAND, CityEnum.NASHVILLE, 17),
                ObjectiveCard(CityEnum.SAN_FRANCISCO, CityEnum.ATLANTA, 17),
                ObjectiveCard(CityEnum.SEATTLE, CityEnum.NEW_YORK, 22),
                ObjectiveCard(CityEnum.LOS_ANGELES, CityEnum.MIAMI, 20),
                ObjectiveCard(CityEnum.SEATTLE, CityEnum.LOS_ANGELES, 9),
                ObjectiveCard(CityEnum.DULUTH, CityEnum.HOUSTON, 8),
                ObjectiveCard(CityEnum.MONTREAL, CityEnum.ATLANTA, 9),
                ObjectiveCard(CityEnum.MONTREAL, CityEnum.NEW_ORLEANS, 13),
                ObjectiveCard(CityEnum.CALGARY, CityEnum.PHOENIX, 13),
                ObjectiveCard(CityEnum.DALLAS, CityEnum.NEW_YORK, 11),
                ObjectiveCard(CityEnum.VANCOUVER, CityEnum.SANTA_FE, 13),
                ObjectiveCard(CityEnum.WINNIPEG, CityEnum.HOUSTON, 12),
                ObjectiveCard(CityEnum.CALGARY, CityEnum.SALT_LAKE_CITY, 7),
                ObjectiveCard(CityEnum.VANCOUVER, CityEnum.MONTREAL, 20),
                ObjectiveCard(CityEnum.LOS_ANGELES, CityEnum.CHICAGO, 16),
                ObjectiveCard(CityEnum.PORTLAND, CityEnum.PHOENIX, 11),
                ObjectiveCard(CityEnum.SAULT_STE_MARIE, CityEnum.OKLAHOMA_CITY, 9),
                ObjectiveCard(CityEnum.DULUTH, CityEnum.EL_PASO, 10),
                ObjectiveCard(CityEnum.CHICAGO, CityEnum.NEW_ORLEANS, 7),
                ObjectiveCard(CityEnum.BOSTON, CityEnum.MIAMI, 12)
            ]
        )


class TrainCardsDeck(Deck):
    def __init__(self, empty: bool):
        if empty:
            super().__init__([])
        else:
            train_cards = []
            for color in TrainColor:
                for _ in range(color.value[1]):
                    train_cards.append(TrainCard(color))
            super().__init__(train_cards)


class PlayerColors(Enum):
    def _generate_next_value_(name, start, count, last_values):
        ...
        return name.lower()
    RED = auto()
    BLUE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLACK = auto()


class Pawn:
    def __init__(self, _color: PlayerColors):
        self.color = _color


class Player:
    def __init__(self, _color: PlayerColors, _order: int):
        self.color = _color
        self.cards = TrainCardsDeck(empty=True)
        self.objectives = ObjectiveCardsDeck()
        self.pawns = [Pawn(self.color) for _ in range(45)]
        self.score = 0
        self.order = _order
        self.str_type = "User"
        self.completed_objectives_count = 0

    def __str__(self):
        return f"Player #{self.order} ({self.str_type}) color : {self.color.value}"

    def __gt__(self, other):
        # Order for first player list sort
        if self.score == other.score and self.score == 0:
            return self.order > other.score

        if self.score != other.score:
            return self.score > other.score

        if self.score == other.score:
            if self.completed_objectives_count != other.completed_objectives_count:
                return self.completed_objectives_count > other.completed_objectives_count

            else:
                # Longest railway
                pass

    def __le__(self, other):
        return not (self > other)


class AIPlayer(Player):
    def __init__(self, _color: PlayerColors, _order: int):
        super().__init__(_color, _order)
        self.str_type = "AI"


class Game:
    def __init__(self, n_player: int, n_ai: int):
        self.player_total = n_player
        self.ai_count = n_ai

        self.train_cards_deck = TrainCardsDeck(empty=False)
        self.discarded_train_cards = TrainCardsDeck(empty=True)
        self.objective_cards_deck = ObjectiveCardsDeck()
        self.players = []

        self.init_players()

    def init_players(self):
        n_players = self.player_total - self.ai_count
        color_list = [color for color in PlayerColors]
        order_list = [i+1 for i in range(self.player_total)]
        rd.shuffle(color_list)
        rd.shuffle(order_list)
        for i in range(n_players):
            self.players.append(Player(color_list.pop(), order_list[i]))

        for i in range(self.ai_count):
            self.players.append(AIPlayer(color_list.pop(), order_list[i]))

        for player in self.players:
            print(player)
