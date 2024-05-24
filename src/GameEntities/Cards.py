from src.Enumeration import TrainCardColorEnum, CityEnum
import random as rd

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


class VisibleTrainCardsDeck(TrainCardsDeck):
    def __init__(self):
        super().__init__(empty=True)

    def get(self, i: int):
        return self.cards.pop(i)