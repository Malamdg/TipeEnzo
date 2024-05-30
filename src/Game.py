import random as rd
from src.GameEntities.Cards import TrainCardsDeck, ObjectiveCardsDeck, VisibleTrainCardsDeck
from src.GameEntities.Board import Board
from src.Players import Player, AIPlayer
from src.Enumeration import PlayerColorEnum
from src.GameEntities.Score import Score


# --- Utils

def trigger_last_turn(player: Player):
    """
    Return whether player triggers last turn
    :return:
    """
    return len(player.pawns) > 2


# --- Game object

class Game:
    def __init__(self, n_player: int, n_ai: int):
        # --- Player stats
        self.player_total = n_player + n_ai
        self.ai_count = n_ai

        # --- Game resources
        self.train_cards_deck = TrainCardsDeck(empty=False)
        self.visible_train_cards_deck = VisibleTrainCardsDeck(empty=True)
        self.discarded_train_cards = TrainCardsDeck(empty=True)
        self.objective_cards_deck = ObjectiveCardsDeck(empty=False)
        self.board = Board()

        # --- Players
        self.players = []

        self.init_players()

    def init_players(self):
        """
        Init player entities

        :return:
        """
        n_players = self.player_total - self.ai_count
        color_list = [color for color in PlayerColorEnum]
        order_list = [i + 1 for i in range(self.player_total)]
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

    def play(self):
        """
        Main function of the game

        :return:
        """
        game_finished = False

        while not game_finished:
            # Implement turn handling and stop cases
            for player in self.players:
                self.player_turn(player)
                # Handle stop case
                if trigger_last_turn(player):
                    # Set game_finished to true
                    game_finished = True
                    # Reorder players
                    self.update_turn_orders(player)

                    # Play last turn
                    for p in self.players:
                        self.player_turn(p)

                    # End of the game
                    break

    def player_turn(self, player: Player):
        """
        Do the turn of the player

        :param player:
        :return:
        """
        choice = input(print("For your 2nd card\n"
                             ""
                             "#=================================================#\n"
                             "# You have the choice between the following:      #\n"
                             "# \t1 - Draw a train card                         #\n"
                             "# \t2 - Draw an Objective card                    #\n"
                             "# \t3 - Occupy a road                             #\n"
                             "#=================================================#"))
        if choice == 1:
            c = player.draw_train_card(self.train_cards_deck, self.visible_train_cards_deck, self.discarded_train_cards)
            if c == player.change_str:
                return self.player_turn(player)
        elif choice == 2:
            c = player.draw_objective_card(self.objective_cards_deck)
            if c == player.change_str:
                return self.player_turn(player)
        elif choice == 3:
            c = player.place_train_pawns(Board, self.discarded_train_cards, Score)
            if c == player.change_str:
                return self.player_turn(player)


    def update_turn_orders(self, last_player: Player):
        """
        Reorder players by setting their turn_order and re-oder self.players accordingly

        :param last_player:
        :return:
        """

        last_player_index = last_player.turn_order
        delta = self.player_total - last_player_index
        reordered_players = [i for i in range(self.player_total)]

        # Reorder players
        for player in self.players:
            new_turn_order = (player.turn_order + delta) % self.player_total
            player.turn_order = self.player_total if new_turn_order == 0 else new_turn_order  # ternary operator
            reordered_players[player.turn_order - 1] = player  # turn orders are 1 based so reindex

        self.players = reordered_players
