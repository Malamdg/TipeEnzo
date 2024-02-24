from classes import Game


def main():
    """
    Main function for project
    :return:
    """
    print("=============== Ticket To Ride =================")
    user_input = str(input("Start game ? (y/n) \n"))
    # Setup game
    player_count_ok = False
    n_player = -1

    while not player_count_ok:
        if user_input.lower().strip() != "y":
            return
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
                        return
            # Case 2 : Too few player selected
            else:
                print("Too few players selected")
                user_input = str(input("Continue ? (y/n) \n"))
                if user_input.lower().strip() != "y":
                    return

    ai_count_ok = False
    n_ai = -1
    while not ai_count_ok:
        n_ai = int(input("How much AI players ? : "))

        if n_ai < 0:
            n_ai = 0

        # -- Input check --
        ai_count_ok = n_player >= n_ai

        # Too many AI players selected
        if n_ai > n_player:
            user_input = str(
                input(f"Too much AI players selected : {n_ai}, would you like to reselect AI players count ? (y/n) \n")
            )
            n_ai = 0

            if user_input.lower().strip() != "y":
                user_input = str(input("Continue with no AI player ? (y/n) \n"))
                if user_input.lower().strip() == "y":
                    ai_count_ok = True

    n = n_player - n_ai
    message = f"{n} players and {n_ai} AI players"

    if n == 0:
        message = f"{n_player} AI players"

    if n == n_player:
        message = f"{n_player} players"

    print(f"Starting game with {message}")

    game = Game(n_player, n_ai)
    print(f"game.player_total = {game.player_total}")


if __name__ == '__main__':
    main()
