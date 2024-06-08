import random as rd
import time

from src.Players import *
from src.Enumeration import PlayerColorEnum
from src.Utils.Math import Algorithm
import os


# --- Utils

def trigger_last_turn(player: Player):
    """
    Return whether player triggers last turn
    :return:
    """
    return len(player.pawns) < 2


# --- Game object

class Game:
    def __init__(self, n_player: int, n_ai: int):
        # --- Player stats
        self.player_total = n_player + n_ai
        self.ai_count = n_ai

        # --- Game resources
        self.train_cards_deck = TrainCardsDeck(empty=False)
        self.visible_train_cards_deck = VisibleTrainCardsDeck()
        self.discarded_train_cards = TrainCardsDeck(empty=True)
        self.objective_cards_deck = ObjectiveCardsDeck(empty=False)
        self.board = Board()

        # --- Players
        self.players = []
        self.winner = None
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

        ai_players_list = [
            "balanced",
            "base",
            "defensive",
            "greedy",
            "random"
        ]
        # Add random AI players
        for i in range(self.ai_count):
            player = ai_players_list.pop(rd.randrange(len(ai_players_list)))
            if player == "balanced":
                self.players.append(BalancedAIPlayer(color_list.pop(), order_list.pop()))
                continue

            if player == "base":
                self.players.append(AIPlayer(color_list.pop(), order_list.pop()))
                continue

            if player == "defensive":
                self.players.append(DefensiveAIPlayer(color_list.pop(), order_list.pop()))
                continue

            if player == "greedy":
                self.players.append(GreedyAIPlayer(color_list.pop(), order_list.pop()))
                continue

            if player == "random":
                self.players.append(RandomAIPlayer(color_list.pop(), order_list.pop()))
                continue

        self.players.sort()
        rd.shuffle(self.train_cards_deck.cards)
        self.visible_train_cards_deck.refill_cards(self.discarded_train_cards, self.train_cards_deck)
        # Display starting player order
        for player in self.players:
            for _ in range(4):
                player.cards.add_card(self.train_cards_deck.draw())
            print(player)

    def play(self):
        """
        Main function of the game

        :return:
        """
        for player in self.players:
            player.draw_objective_card(self.objective_cards_deck, True)

        game_finished = False
        while not game_finished:
            # Implement turn handling and stop cases
            for player in self.players:
                player.play_turn(
                    self.board,
                    self.objective_cards_deck,
                    self.train_cards_deck,
                    self.visible_train_cards_deck,
                    self.discarded_train_cards
                )
                # Handle stop case
                if trigger_last_turn(player):
                    # Set game_finished to true
                    game_finished = True
                    # Reorder players
                    self.update_turn_orders(player)

                    # Play last turn
                    for p in self.players:
                        p.play_turn(
                            self.board,
                            self.objective_cards_deck,
                            self.train_cards_deck,
                            self.visible_train_cards_deck,
                            self.discarded_train_cards
                        )

                    # End of the game
                    break

        self.endgame()

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

    def endgame(self):
        # Handle the longest railway bonus card
        max_length = 0
        tie_players = []

        for player in self.players:
            longest_road = Algorithm.longest_road(player)
            if longest_road > max_length:
                max_length = longest_road
                tie_players = []

            if longest_road == max_length:
                tie_players.append(player)

        for player in tie_players:
            player.score.value += 10

        # Handle objective cards
        for player in self.players:
            for objective_card in player.objectives.cards:
                if objective_card is None:
                    continue
                player.score.value += objective_card.get_value()

        # Sort by score and get the winner
        self.players.sort()
        self.winner = self.players[0]

        print(f"Winner : {self.winner.__str__()}! \n")
        i = 1
        for player in self.players:
            print(f"#{i} {player.__str__()} ")
            i += 1


class TrainingGame(Game):
    def __init__(self, n_player, n_ai, ai_trainer):
        super().__init__(n_player, n_ai)
        self.ai_trainer = ai_trainer
        self.model_data_path = os.path.join('src', 'Data', 'data.csv')

    def play(self):
        """
        Main function of the game

        :return:
        """
        start_time = time.time()
        for player in self.players:
            player.draw_objective_card(self.objective_cards_deck, True)

        game_finished = False
        self.ai_trainer.clear_data()
        while not game_finished:

            # Implement turn handling and stop cases
            for player in self.players:
                state = self.get_game_state(player)
                action = player.play_turn(
                    self.board,
                    self.objective_cards_deck,
                    self.train_cards_deck,
                    self.visible_train_cards_deck,
                    self.discarded_train_cards
                )
                self.ai_trainer.log_state_action(state, action)

                # Handle stop case
                if trigger_last_turn(player):
                    # Set game_finished to true
                    game_finished = True
                    # Reorder players
                    self.update_turn_orders(player)

                    # Play last turn
                    for _player in self.players:
                        state = self.get_game_state(player)
                        action = _player.play_turn(
                            self.board,
                            self.objective_cards_deck,
                            self.train_cards_deck,
                            self.visible_train_cards_deck,
                            self.discarded_train_cards
                        )
                        self.ai_trainer.log_state_action(state, action)

                    # End of the game
                    break

        self.endgame()
        self.ai_trainer.save_data(self.model_data_path)

    def get_game_state(self, player):
        state = {
            'player_total': len(self.players),
            'player_turn': player.turn_order,
            'objective_cards_count': len(player.objectives.cards),
            'train_cards_count': len(player.cards.cards),
            'visible_train_cards_count': len(self.visible_train_cards_deck.cards),
            'pawn_count': len(player.pawns),
            'score': player.score.value
        }
        return state


class MLVsAI(Game):
    """
    Show up MLBasedAIPlayer training
    """

    def init_players(self):
        ai_players_list = [
            "balanced",
            "base",
            "defensive",
            "greedy",
            "random"
        ]

        rd.shuffle(ai_players_list)
        ai_players_list.pop()

        # Index of ml player
        ml_id = rd.randrange(self.player_total)

        color_list = [color for color in PlayerColorEnum]
        rd.shuffle(color_list)

        for i in range(self.player_total):
            if i == ml_id:
                self.players.append(MLBasedAIPlayer(color_list.pop(), i + 1))
                continue

            player = ai_players_list.pop(rd.randrange(len(ai_players_list)))
            if player == "balanced":
                self.players.append(BalancedAIPlayer(color_list.pop(), i + 1))
                return

            if player == "base":
                self.players.append(AIPlayer(color_list.pop(), i + 1))
                return

            if player == "defensive":
                self.players.append(DefensiveAIPlayer(color_list.pop(), i + 1))
                return

            if player == "greedy":
                self.players.append(GreedyAIPlayer(color_list.pop(), i + 1))
                return

            if player == "random":
                self.players.append(RandomAIPlayer(color_list.pop(), i + 1))
                return
