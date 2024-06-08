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
        self.completed = False

    def set_completed(self):
        self.completed = True

    def get_value(self):
        direction = 1 if self.completed else -1
        return self.points * direction

    def __str__(self):
        return f"From {self.start.value.capitalize()} to {self.destination.value.capitalize()} | {self.points}pts"


class Deck:
    def __init__(self, cards: list):
        self.cards = cards

    def shuffle(self):
        cards = self.cards
        # shuffle algorithm
        rd.shuffle(cards)
        self.cards = cards

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

    def count_by_color(self):
        color_count_dict = {}
        for card in self.cards:
            if card not in color_count_dict:
                color_count_dict[card.color.value[0]] = 1
                continue
            color_count_dict[card.color.value[0]] += 1
        return color_count_dict


class VisibleTrainCardsDeck(TrainCardsDeck):
    def __init__(self):
        super().__init__(empty=True)

    def get(self, i: int):
        return self.cards.pop(i)

    def refill_cards(self, discarded_deck: TrainCardsDeck, deck: TrainCardsDeck):
        # Not enough cards to apply rule
        if len(self.cards) + len(deck.cards) + len(discarded_deck.cards) <= 5:
            discarded_deck.shuffle()
            deck.merge_decks(discarded_deck)
            self.merge_decks(deck)
            return
        # Apply rule 3 visible jokers => discard all and refill
        while len(self.cards) != 5:
            self.add_card(deck.draw())
            if len(deck.cards) == 0:
                discarded_deck.shuffle()
                deck.merge_decks(discarded_deck)
        color_dict = self.count_by_color()
        if (TrainCardColorEnum.JOKER.value[0] in color_dict.keys()
                and color_dict[TrainCardColorEnum.JOKER.value[0]] == 3):
            discarded_deck.merge_decks(self)
            self.refill_cards(discarded_deck, deck)
