# Import necessary components from the provided code
from src.Enumeration import CityEnum, PlayerColorEnum
from src.GameEntities.Board import Board
from Math import Algorithm
from src.Players import Player
import random
import matplotlib.pyplot as plt


def plot_board(board, player=None):
    # Define city positions for visualization (mock coordinates for demonstration)
    city_positions = {
        CityEnum.VANCOUVER: (1, 9),
        CityEnum.CALGARY: (3, 8),
        CityEnum.WINNIPEG: (6, 8),
        CityEnum.SAULT_STE_MARIE: (9, 7),
        CityEnum.MONTREAL: (12, 6),
        CityEnum.BOSTON: (14, 6),
        CityEnum.NEW_YORK: (14, 4),
        CityEnum.TORONTO: (10, 6),
        CityEnum.SEATTLE: (1, 7),
        CityEnum.HELENA: (5, 5),
        CityEnum.DULUTH: (7, 6),
        CityEnum.OMAHA: (5, 4),
        CityEnum.DENVER: (3, 3),
        CityEnum.SALT_LAKE_CITY: (2, 3),
        CityEnum.SAN_FRANCISCO: (0, 2),
        CityEnum.LOS_ANGELES: (0, 1),
        CityEnum.ATLANTA: (12, 2),
        CityEnum.MIAMI: (14, 1),
        CityEnum.HOUSTON: (8, 1),
        CityEnum.NEW_ORLEANS: (9, 2),
        CityEnum.DALLAS: (7, 1),
        CityEnum.EL_PASO: (4, 1),
        CityEnum.SANTA_FE: (3, 2),
        CityEnum.PHOENIX: (2, 1),
        CityEnum.OKLAHOMA_CITY: (6, 2),
        CityEnum.KANSAS_CITY: (5, 2),
        CityEnum.SAINT_LOUIS: (8, 4),
        CityEnum.PITTSBURGH: (12, 4),
        CityEnum.WASHINGTON: (13, 3),
        CityEnum.RALEIGH: (12, 3),
        CityEnum.NASHVILLE: (11, 3),
        CityEnum.CHARLESTON: (13, 2),
        CityEnum.LITTLE_ROCK: (8, 3),
        CityEnum.CHICAGO: (7, 5),
        CityEnum.PORTLAND: (1, 6),
        CityEnum.LAS_VEGAS: (1, 1),
    }

    fig, ax = plt.subplots()
    for road in board.roads:
        start_pos = city_positions[road.start]
        end_pos = city_positions[road.end]
        if player:
            color = 'grey' if not road.occupied or road.occupier != player else player.color.name.lower()
        else:
            color = 'grey' if not road.occupied else road.occupier.color.name.lower()
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], color=color, lw=2)

    for city, pos in city_positions.items():
        ax.scatter(*pos, s=100, color='black')
        ax.text(pos[0], pos[1], city.name, fontsize=9, ha='right')

    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.show()


def test_longest_road():
    # Initialize players with random turn order
    players = [
        Player(PlayerColorEnum.RED, _turn_order=random.randint(1, 5)),
        Player(PlayerColorEnum.BLUE, _turn_order=random.randint(1, 5)),
        Player(PlayerColorEnum.GREEN, _turn_order=random.randint(1, 5)),
        Player(PlayerColorEnum.YELLOW, _turn_order=random.randint(1, 5)),
        Player(PlayerColorEnum.BLACK, _turn_order=random.randint(1, 5))
    ]

    # Number of players for the test (between 2 and 5)
    num_players = random.randint(2, 5)
    active_players = players[:num_players]

    # Initialize board
    board = Board()

    # Simulate road occupations
    roads = board.roads
    random.shuffle(roads)  # Shuffle roads to simulate random occupation

    # Distribute roads among active players
    for i, road in enumerate(roads):
        if i >= len(roads) * 0.6:  # Occupy about 60% of the roads to leave some unoccupied
            break
        player = active_players[i % num_players]
        road.occupy(player)

    # Visualize the board
    plot_board(board)

    # Calculate and visualize longest road for each player
    for player in active_players:
        longest_road_length = Algorithm.player_longest_road(player, board)
        print(f"Longest road for Player {player.color.name} : {longest_road_length}")
        plot_board(board, player)


if __name__ == "__main__":
    # Run the test function
    test_longest_road()
