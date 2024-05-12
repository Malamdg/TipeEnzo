from src.Enumeration import CityEnum, TrainCardColorEnum
from src.Players import Player


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
