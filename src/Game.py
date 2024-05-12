import random as rd
from src.GameEntities.Cards import TrainCardsDeck, ObjectiveCardsDeck
from src.Players import Player, AIPlayer
from src.Enumeration import PlayerColorEnum


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
