import random as rd
from enum import *


# -------------------- #
# --- ENUMERATIONS --- #
# -------------------- #


class TrainCardColorEnum(Enum):
    BLACK = "black", 12
    BLUE = "blue", 12
    GREEN = "green", 12
    JOKER = "joker", 14
    ORANGE = "orange", 12
    PINK = "pink", 12
    RED = "red", 12
    YELLOW = "yellow", 12
    WHITE = "white", 12


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


class PlayerColorEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        ...
        return name.lower()
    RED = auto()
    BLUE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLACK = auto()

# -------------------- #
# --- CARD CLASSES --- #
# -------------------- #


class Card:
    def __init__(self):
        return


class TrainCard(Card):
    def __init__(self, color: TrainCardColorEnum):
        super().__init__()
        self.color = color

    def __str__(self):
        return f"{self.color.value[0]} train card"


class ObjectiveCard(Card):
    def __init__(self, start_city, destination_city, points):
        super().__init__()
        self.start = start_city
        self.destination = destination_city
        self.points = points

    def __str__(self):
        return f"From {self.start} to {self.destination} | {self.points}pts"


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


class ObjectiveCardsDeck(Deck):
    def __init__(self, empty: bool):
        if empty:
            super().__init__([])
        else:
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
            for color in TrainCardColorEnum:
                for _ in range(color.value[1]):
                    train_cards.append(TrainCard(color))
            super().__init__(train_cards)


# --------------------- #
# --- Game Entities --- #
# --------------------- #

class Pawn:
    def __init__(self, _color: PlayerColorEnum):
        self.color = _color


class Player:
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        # --- Attributes
        self.str_type = "User"
        self.color = _color

        # --- Resources
        self.cards = TrainCardsDeck(empty=True)
        self.objectives = ObjectiveCardsDeck(empty=True)
        self.pawns = [Pawn(self.color) for _ in range(45)]

        # --- In game - functional
        self.turn_order = _turn_order
        self.score = 0
        self.completed_objectives_count = 0

    # --- Game actions

    def draw_objective_card(self, source: ObjectiveCardsDeck):
        """
        A player draws 3 objective cards and must keep at least 1
        :param source:
        :return:
        """

        # Cards to add to user's
        kept_cards = ObjectiveCardsDeck(empty=True)
        # Cards to put at source's bottom
        discarded_cards = ObjectiveCardsDeck(empty=True)

        # --- Interaction with game object

        # Draw cards
        drawn_cards = [source.draw() for _ in range(3)]

        # --- Player Interaction

        # Display cards
        print("Here are your drawn objectives: \n")
        i = 0
        for card in drawn_cards:
            i += 1
            msg = f"#{i} {card.__str__()} \n"
            print(msg)

        # Get which card to keep
        response = str(
            input(
                "Chose which card(s) you want to keep ? (at least one, separate choices with an empty space):"
            )
        )

        # Intended response format: "1 2 3"
        # Will give: [0,1,2] the indexes in the card list
        indexes = [int(el.strip()) - 1 for el in response.split(" ")]

        # --- Final treatment

        # function to split drawn_cards in each category
        def split_cards(index, el):
            if index in indexes:
                kept_cards.add_card(el)
            else:
                discarded_cards.add_card(el)

        # Apply split function on drawn_cards
        map(split_cards, drawn_cards)

        # Add cards to respective decks
        self.objectives.merge_decks(kept_cards)
        source.merge_decks(discarded_cards)

    def draw_train_card(self, source: TrainCardsDeck):
        """
        A player draws 2 cards
        Todo implement function
        :param source:
        :return:
        """

    # --- Operators
    def __str__(self):
        return f"Player #{self.turn_order} ({self.str_type}) color : {self.color.value}"

    def __lt__(self, other):
        if self.score == other.score:
            # First sort
            if self.score == 0:
                return self.turn_order < other.turn_order

            if self.completed_objectives_count == other.completed_objectives_count:
                # Longest railway
                pass

            return self.completed_objectives_count < other.completed_objectives_count

        return self.score < other.score

    def __gt__(self, other):
        if self.score == other.score:
            # First sort
            if self.score == 0:
                return self.turn_order > other.turn_order

            if self.completed_objectives_count == other.completed_objectives_count:
                # Longest railway
                pass

            return self.completed_objectives_count > other.completed_objectives_count

        return self.score > other.score

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        return self.__ge__(other) and self.__le__(other)


class AIPlayer(Player):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "AI"


class Game:
    def __init__(self, n_player: int, n_ai: int):
        self.player_total = n_player + n_ai
        self.ai_count = n_ai

        self.train_cards_deck = TrainCardsDeck(empty=False)
        self.discarded_train_cards = TrainCardsDeck(empty=True)
        self.objective_cards_deck = ObjectiveCardsDeck(empty=False)
        self.players = []

        self.init_players()

    def init_players(self):
        n_players = self.player_total - self.ai_count
        color_list = [color for color in PlayerColorEnum]
        order_list = [i+1 for i in range(self.player_total)]
        rd.shuffle(color_list)
        rd.shuffle(order_list)
        for i in range(n_players):
            self.players.append(Player(color_list.pop(), order_list.pop()))

        for i in range(self.ai_count):
            self.players.append(AIPlayer(color_list.pop(), order_list.pop()))

        self.players.sort()

        # Display starting player order
        for player in self.players:
            print(player)
