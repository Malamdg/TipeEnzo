from src.Game import Game, TrainingGame
import random
import os
from src.Utils.AiTrainer import TicketToRideTrainAI


class App:
    """
    Abstract App class
    """
    def run(self):
        pass


class TicketToRide(App):
    def __init__(self, add_bots: bool):
        self.handle_ai = add_bots

    def run(self):
        print("=============== Ticket To Ride =================")
        user_input = str(input("Start game ? (y/n) \n"))

        if user_input.lower().strip() != "y":
            return

        # Setup game
        n_player = self.handle_total_player_count()

        # If -1 returned => break
        if n_player == -1:
            return

        n_ai = 0

        message = f"{n_player} players"

        # Add bot players if needed
        if self.handle_ai:
            n_ai = self.handle_ai_player_count(n_player)

            n = n_player - n_ai
            message = f"{n} players and {n_ai} AI players"

            if n == 0:
                message = f"{n_player} AI players"

            if n == n_player:
                message = f"{n_player} players"

        print(f"Starting game with {message}")

        game = Game(n_player, n_ai)
        print(f"game.player_total = {game.player_total}")
        game.play()

    @staticmethod
    def handle_total_player_count():
        player_count_ok = False
        n_player = -1
        while not player_count_ok:
            n_player = int(input("How much players ? : "))

            # -- Input check --
            player_count_ok = 2 <= n_player <= 5

            if not player_count_ok:
                # Case 1 : Too many players selected
                if n_player > 5:
                    user_input = str(
                        input(f"Too much players selected : {n_player} starting the game with 5 players ? (y/n) \n")
                    )
                    n_player = 5

                    if user_input.lower().strip() != "y":
                        user_input = str(input("Continue ? (y/n) \n"))
                        if user_input.lower().strip() != "y":
                            return -1
                # Case 2 : Too few player selected
                else:
                    print("Too few players selected")
                    user_input = str(input("Continue ? (y/n) \n"))
                    if user_input.lower().strip() != "y":
                        return -1

        return n_player

    @staticmethod
    def handle_ai_player_count(total_player_count: int):
        ai_count_ok = False
        n_ai = -1
        while not ai_count_ok:
            n_ai = int(input("How much AI players ? : "))

            if n_ai < 0:
                n_ai = 0

            # -- Input check --
            ai_count_ok = total_player_count >= n_ai

            # Too many AI players selected
            if n_ai > total_player_count:
                user_input = str(
                    input(
                        f"Too much AI players selected : {n_ai}, would you like to reselect AI players count ? (y/n) \n"
                    )
                )
                n_ai = 0

                if user_input.lower().strip() != "y":
                    user_input = str(input("Continue with no AI player ? (y/n) \n"))
                    if user_input.lower().strip() == "y":
                        ai_count_ok = True
        return n_ai


class TicketToRideNoAi(TicketToRide):
    def __init__(self):
        super().__init__(False)


class TicketToRideTrainAi(TicketToRide):
    def __init__(self):
        super().__init__(True)
        self.model_data_path = os.path.join('src', 'Data', 'data.csv')

    def run(self):
        n_games = int(input("How many training games ? : "))
        ai_trainer = TicketToRideTrainAI()
        ai_trainer.clear_data()
        for i in range(n_games):
            print(f"Game #{i+1} \n")
            n_ai = random.randint(2, 5)  # Random number of AI player
            game = TrainingGame(n_player=0, n_ai=n_ai, ai_trainer=ai_trainer)
            game.play()
        ai_trainer.save_data(self.model_data_path)
