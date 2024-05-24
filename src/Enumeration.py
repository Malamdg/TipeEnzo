from enum import *


# -------------------- #
# --- Enumerations --- #
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
    WASHINGTON = "Washington"
    OMAHA = "Omaha"
    RALEIGH = "Raleigh"
    SAINT_LOUIS = "Saint Louis"
    LAS_VEGAS = "Las Vegas"
    CHARLESTON = "Charleston"


class PlayerColorEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        ...
        return name.lower()

    RED = auto()
    BLUE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLACK = auto()
