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
            Road(CityEnum.BOSTON, CityEnum.NEW_YORK, 2, TrainCardColorEnum.YELLOW),
            Road(CityEnum.BOSTON, CityEnum.NEW_YORK, 2, TrainCardColorEnum.RED),
            Road(CityEnum.MONTREAL, CityEnum.NEW_YORK, 3, TrainCardColorEnum.BLUE),
            Road(CityEnum.MONTREAL, CityEnum.TORONTO, 3),
            Road(CityEnum.VANCOUVER, CityEnum.SEATTLE, 1),
            Road(CityEnum.VANCOUVER, CityEnum.SEATTLE, 1),
            Road(CityEnum.SEATTLE, CityEnum.CALGARY, 4),
            Road(CityEnum.SEATTLE, CityEnum.HELENA, 6, TrainCardColorEnum.YELLOW),
            Road(CityEnum.SEATTLE, CityEnum.PORTLAND, 1),
            Road(CityEnum.SEATTLE, CityEnum.PORTLAND, 1),
            Road(CityEnum.CALGARY, CityEnum.HELENA, 4),
            Road(CityEnum.HELENA, CityEnum.WINNIPEG, 4, TrainCardColorEnum.BLUE),
            Road(CityEnum.HELENA, CityEnum.DULUTH, 6, TrainCardColorEnum.ORANGE),
            Road(CityEnum.HELENA, CityEnum.OMAHA, 5, TrainCardColorEnum.RED),
            Road(CityEnum.HELENA, CityEnum.DENVER, 4, TrainCardColorEnum.GREEN),
            Road(CityEnum.HELENA, CityEnum.SALT_LAKE_CITY, 3, TrainCardColorEnum.PINK),
            Road(CityEnum.PORTLAND, CityEnum.SALT_LAKE_CITY, 6, TrainCardColorEnum.BLUE),
            Road(CityEnum.PORTLAND, CityEnum.SAN_FRANCISCO, 5, TrainCardColorEnum.GREEN),
            Road(CityEnum.PORTLAND, CityEnum.SAN_FRANCISCO, 5, TrainCardColorEnum.PINK),
            Road(CityEnum.OMAHA, CityEnum.DENVER, 4, TrainCardColorEnum.PINK),
            Road(CityEnum.OMAHA, CityEnum.KANSAS_CITY, 1),
            Road(CityEnum.OMAHA, CityEnum.KANSAS_CITY, 1),
            Road(CityEnum.WINNIPEG, CityEnum.DULUTH, 4, TrainCardColorEnum.BLACK),
            Road(CityEnum.DULUTH, CityEnum.TORONTO, 6, TrainCardColorEnum.PINK),
            Road(CityEnum.DULUTH, CityEnum.CHICAGO, 3, TrainCardColorEnum.RED),
            Road(CityEnum.DULUTH, CityEnum.OMAHA, 2),
            Road(CityEnum.DULUTH, CityEnum.OMAHA, 2),
            Road(CityEnum.SAULT_STE_MARIE, CityEnum.TORONTO, 2),
            Road(CityEnum.TORONTO, CityEnum.PITTSBURGH, 2),
            Road(CityEnum.TORONTO, CityEnum.CHICAGO, 4, TrainCardColorEnum.WHITE),
            Road(CityEnum.NEW_YORK, CityEnum.PITTSBURGH, 2, TrainCardColorEnum.WHITE),
            Road(CityEnum.NEW_YORK, CityEnum.PITTSBURGH, 2, TrainCardColorEnum.GREEN),
            Road(CityEnum.NEW_YORK, CityEnum.WASHINGTON, 2, TrainCardColorEnum.ORANGE),
            Road(CityEnum.NEW_YORK, CityEnum.WASHINGTON, 2, TrainCardColorEnum.BLACK),
            Road(CityEnum.PITTSBURGH, CityEnum.WASHINGTON, 2),
            Road(CityEnum.PITTSBURGH, CityEnum.RALEIGH, 2),
            Road(CityEnum.PITTSBURGH, CityEnum.NASHVILLE, 4, TrainCardColorEnum.YELLOW),
            Road(CityEnum.PITTSBURGH, CityEnum.SAINT_LOUIS, 4, TrainCardColorEnum.YELLOW),
            Road(CityEnum.CHICAGO, CityEnum.PITTSBURGH, 3, TrainCardColorEnum.ORANGE),
            Road(CityEnum.CHICAGO, CityEnum.PITTSBURGH, 3, TrainCardColorEnum.BLACK),
            Road(CityEnum.CHICAGO, CityEnum.SAINT_LOUIS, 2, TrainCardColorEnum.GREEN),
            Road(CityEnum.CHICAGO, CityEnum.SAINT_LOUIS, 2, TrainCardColorEnum.WHITE),
            Road(CityEnum.OMAHA, CityEnum.DENVER, 4, TrainCardColorEnum.PINK),
            Road(CityEnum.OMAHA, CityEnum.KANSAS_CITY, 1),
            Road(CityEnum.OMAHA, CityEnum.KANSAS_CITY, 1),
            Road(CityEnum.SAN_FRANCISCO, CityEnum.SALT_LAKE_CITY, 5, TrainCardColorEnum.ORANGE),
            Road(CityEnum.SAN_FRANCISCO, CityEnum.SALT_LAKE_CITY, 5, TrainCardColorEnum.WHITE),
            Road(CityEnum.SAN_FRANCISCO, CityEnum.LOS_ANGELES, 3, TrainCardColorEnum.PINK),
            Road(CityEnum.SAN_FRANCISCO, CityEnum.LOS_ANGELES, 3, TrainCardColorEnum.YELLOW),
            Road(CityEnum.SALT_LAKE_CITY, CityEnum.DENVER, 3, TrainCardColorEnum.RED),
            Road(CityEnum.SALT_LAKE_CITY, CityEnum.DENVER, 3, TrainCardColorEnum.YELLOW),
            Road(CityEnum.SALT_LAKE_CITY, CityEnum.LAS_VEGAS, 3, TrainCardColorEnum.ORANGE),
            Road(CityEnum.DENVER, CityEnum.PHOENIX, 5, TrainCardColorEnum.WHITE),
            Road(CityEnum.DENVER, CityEnum.SANTA_FE, 2),
            Road(CityEnum.DENVER, CityEnum.OKLAHOMA_CITY, 4, TrainCardColorEnum.RED),
            Road(CityEnum.DENVER, CityEnum.KANSAS_CITY, 4, TrainCardColorEnum.BLACK),
            Road(CityEnum.DENVER, CityEnum.KANSAS_CITY, 4, TrainCardColorEnum.ORANGE),
            Road(CityEnum.KANSAS_CITY, CityEnum.OKLAHOMA_CITY, 2),
            Road(CityEnum.KANSAS_CITY, CityEnum.OKLAHOMA_CITY, 2),
            Road(CityEnum.KANSAS_CITY, CityEnum.SAINT_LOUIS, 2, TrainCardColorEnum.BLUE),
            Road(CityEnum.KANSAS_CITY, CityEnum.SAINT_LOUIS, 2, TrainCardColorEnum.PINK),
            Road(CityEnum.SAINT_LOUIS, CityEnum.NASHVILLE, 2),
            Road(CityEnum.SAINT_LOUIS, CityEnum.LITTLE_ROCK, 2),
            Road(CityEnum.NASHVILLE, CityEnum.LITTLE_ROCK, 3, TrainCardColorEnum.WHITE),
            Road(CityEnum.NASHVILLE, CityEnum.RALEIGH, 3, TrainCardColorEnum.BLACK),
            Road(CityEnum.NASHVILLE, CityEnum.ATLANTA, 1),
            Road(CityEnum.RALEIGH, CityEnum.ATLANTA, 2),
            Road(CityEnum.RALEIGH, CityEnum.ATLANTA, 2),
            Road(CityEnum.RALEIGH, CityEnum.CHARLESTON, 2),
            Road(CityEnum.LAS_VEGAS, CityEnum.LOS_ANGELES, 2),
            Road(CityEnum.SANTA_FE, CityEnum.OKLAHOMA_CITY, 3, TrainCardColorEnum.BLUE),
            Road(CityEnum.SANTA_FE, CityEnum.EL_PASO, 2),
            Road(CityEnum.SANTA_FE, CityEnum.PHOENIX, 3),
            Road(CityEnum.OKLAHOMA_CITY, CityEnum.EL_PASO, 5, TrainCardColorEnum.YELLOW),
            Road(CityEnum.OKLAHOMA_CITY, CityEnum.DALLAS, 2),
            Road(CityEnum.OKLAHOMA_CITY, CityEnum.DALLAS, 2),
            Road(CityEnum.OKLAHOMA_CITY, CityEnum.LITTLE_ROCK, 2),
            Road(CityEnum.LITTLE_ROCK, CityEnum.DALLAS, 2),
            Road(CityEnum.LITTLE_ROCK, CityEnum.NEW_ORLEANS, 3, TrainCardColorEnum.GREEN),
            Road(CityEnum.ATLANTA, CityEnum.CHARLESTON, 2),
            Road(CityEnum.ATLANTA, CityEnum.MIAMI, 5, TrainCardColorEnum.BLUE),
            Road(CityEnum.ATLANTA, CityEnum.NEW_ORLEANS, 4, TrainCardColorEnum.YELLOW),
            Road(CityEnum.ATLANTA, CityEnum.NEW_ORLEANS, 4, TrainCardColorEnum.ORANGE),
            Road(CityEnum.CHARLESTON, CityEnum.MIAMI, 4, TrainCardColorEnum.PINK),
            Road(CityEnum.LOS_ANGELES, CityEnum.EL_PASO, 6, TrainCardColorEnum.BLACK),
            Road(CityEnum.EL_PASO, CityEnum.HOUSTON, 6, TrainCardColorEnum.GREEN),
            Road(CityEnum.DALLAS, CityEnum.EL_PASO, 4, TrainCardColorEnum.RED),
            Road(CityEnum.DALLAS, CityEnum.HOUSTON, 1),
            Road(CityEnum.DALLAS, CityEnum.HOUSTON, 1),
            Road(CityEnum.HOUSTON, CityEnum.NEW_ORLEANS, 2),
            Road(CityEnum.NEW_ORLEANS, CityEnum.MIAMI, 6, TrainCardColorEnum.RED),
        ]
