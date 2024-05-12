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


class VisibleTrainCardsDeck(TrainCardsDeck):
    def __init__(self):
        super().__init__(empty=True)

    def get(self, i: int):
        return self.cards.pop(i)


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

    def draw_train_card(self, deck: TrainCardsDeck, visible_cards: VisibleTrainCardsDeck):
        """
        A player draws 2 cards
        Todo implement function
        :param source:
        :return:
        """

    def draw_from_deck(self, deck: TrainCardsDeck):
        card = deck.draw()
        self.cards.add_card(card)
        print(f"You drew : {card.__str__()}")

    def draw_from_visible_cards(self, visible_cards: VisibleTrainCardsDeck):
        print("Here are the visible cards :")
        i = 0
        for card in visible_cards.cards:
            i += 1
            msg = f"#{i} {card.__str__()} \n"
            print(msg)

        choice = input(
            "Chose which card you want to keep by entering its index :"
        )

        index = int(choice) - 1
        chosen_card = visible_cards.get(index)
        self.cards.add_card(chosen_card)
        print(f"Added card : {chosen_card.__str__()}")

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


class Road:
    def __init__(self, _start: CityEnum, _end: CityEnum, _length: int, _condition=None):
        self.start = _start
        self.end = _end
        self.length = _length
        self.condition = _condition
        self.occupied = False
        self.occupier = None

    def occupy(self, player: Player):
        if self.occupied:
            print(f"Road already occupied by {player.color.value} Player !")
            return -1

        self.occupied = True
        self.occupier = player
        return 0


class Board:
    def __init__(self):
        self.roads = [
            Road(CityEnum.VANCOUVER, CityEnum.CALGARY, 3),
            Road(CityEnum.CALGARY, CityEnum.WINNIPEG, 6, TrainCardColorEnum.WHITE),
            Road(CityEnum.WINNIPEG, CityEnum.SAULT_STE_MARIE, 6),
            Road(CityEnum.SAULT_STE_MARIE, CityEnum.MONTREAL, 5, TrainCardColorEnum.BLACK),
            Road(CityEnum.MONTREAL, CityEnum.BOSTON, 2),
            Road(CityEnum.MONTREAL, CityEnum.BOSTON, 2),
            Road(CityEnum.VANCOUVER, CityEnum.SEATTLE, 1),
            Road(CityEnum.VANCOUVER, CityEnum.SEATTLE, 1),
            Road(CityEnum.SEATTLE, CityEnum.CALGARY, 4),
            Road(CityEnum.SEATTLE, CityEnum.HELENA, 6, TrainCardColorEnum.YELLOW),
            Road(CityEnum.CALGARY, CityEnum.HELENA, 4),
            Road(CityEnum.HELENA, CityEnum.WINNIPEG, 4, TrainCardColorEnum.BLUE),
            Road(CityEnum.HELENA, CityEnum.DULUTH, 6, TrainCardColorEnum.ORANGE),
            Road(CityEnum.WINNIPEG, CityEnum.DULUTH, 4, TrainCardColorEnum.BLACK),
            Road(CityEnum.DULUTH, CityEnum.TORONTO, 6, TrainCardColorEnum.PINK),
            Road(CityEnum.WINNIPEG, CityEnum.DULUTH, 3),
            Road(CityEnum.WINNIPEG, CityEnum.TORONTO, 2),
            Road(CityEnum.MONTREAL, CityEnum.TORONTO, 3),
            Road(CityEnum.MONTREAL, CityEnum.NEW_YORK, 3, TrainCardColorEnum.BLUE),
            Road(CityEnum.BOSTON, CityEnum.NEW_YORK, 2, TrainCardColorEnum.YELLOW),
            Road(CityEnum.BOSTON, CityEnum.NEW_YORK, 2, TrainCardColorEnum.RED),
        ]


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
