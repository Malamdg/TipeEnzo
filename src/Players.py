from src.Enumeration import PlayerColorEnum, TrainCardColorEnum
from src.GameEntities.Board import Road, Board
from src.GameEntities.Cards import TrainCardsDeck, ObjectiveCardsDeck, VisibleTrainCardsDeck
from src.GameEntities.Pawn import Pawn
from src.GameEntities.Score import Score
from src.Utils.Math import Algorithm
import random


class Player:
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        # --- Attributes
        self.str_type = "User"
        self.color = _color

        # --- Resources
        self.cards = TrainCardsDeck(empty=True)
        self.objectives = ObjectiveCardsDeck(empty=True)
        self.pawns = [Pawn(self.color) for _ in range(45)]

        # --- In game - functional
        self.turn_order = _turn_order
        self.change_str = "change action"
        self.score = Score()
        self.completed_objectives_count = 0
        self.roads = []

    # --- Game actions

    def draw_objective_card(self, source: ObjectiveCardsDeck, first_turn=False):
        """
        A player draws 3 objective cards and must keep at least 1
        :param first_turn:
        :param source:
        :return:
        """

        # Cards to add to user's
        kept_cards = ObjectiveCardsDeck(empty=True)
        # Cards to put at source's bottom
        discarded_cards = ObjectiveCardsDeck(empty=True)

        # --- Interaction with game object

        # Draw cards
        drawn_cards = [source.draw() for _ in range(3)]

        # --- Player Interaction

        # Display cards
        print("Here are your drawn objectives: \n")
        i = 0
        for card in drawn_cards:
            i += 1
            msg = f"#{i} {card.__str__()} \n"
            print(msg)

        # Get which card to keep
        if first_turn:
            response = str(
                input(
                    "Chose which card(s) you want to keep ? (at least two, separate choices with an empty space):"
                )
            )
            indexes = [int(el.strip()) - 1 for el in response.split(" ")]
            if len(indexes) < 2:
                print(f"You must keep at least two objectives")
                for card in drawn_cards:
                    source.add_card(card)
                return self.draw_objective_card(source, True)

        else:
            response = str(
                input(
                    "Chose which card(s) you want to keep ? (at least one, separate choices with an empty space):"
                )
            )

        # Intended response format: "1 2 3"
        # Will give: [0,1,2] the indexes in the card list
        indexes = [int(el.strip()) - 1 for el in response.split(" ")]
        if len(indexes) == 0:
            print(f"Please choose at least one of the card here ")
            for card in drawn_cards:
                source.add_card(card)
            return self.draw_objective_card(source, False)

        # --- Final treatment
        # function to split drawn_cards in each category
        def split_cards(index, el):
            if index in indexes:
                kept_cards.add_card(el)
            else:
                discarded_cards.add_card(el)

        # Apply split function on drawn_cards
        map(split_cards, drawn_cards)

        # Add cards to respective decks
        self.objectives.merge_decks(kept_cards)
        source.merge_decks(discarded_cards)

    def draw_train_card(
            self,
            deck: TrainCardsDeck,
            visible_cards: VisibleTrainCardsDeck,
            discarded_cards: TrainCardsDeck
    ):
        """
        A player draws 2 cards

        :param discarded_cards:
        :param deck:
        :param visible_cards:
        :return:
        """
        self.show_visible_card(visible_cards)
        choice = int(
            input(
                "#=================================================#\n"
                "# You have the choice between the following:      #\n"
                "# \t1 - Draw a visible card                       #\n"
                "# \t2 - Draw a face-down card                     #\n"
                "# \t3 - See your hand                             #\n"
                "# \t4 - Change action                             #\n"
                "#=================================================#\n"
            )
        )

        # Draw from visible cards
        if choice == 1:
            self.draw_from_visible_cards(visible_cards, deck, discarded_cards, True)
            visible_cards.refill_cards(discarded_cards, deck)
            if self.cards.cards[-1].color.value[0] == TrainCardColorEnum.JOKER.value[0]:
                return
            choice = int(
                input(
                    "For your 2nd card\n\n"
                    "#=================================================#\n"
                    "# You have the choice between the following:      #\n"
                    "# \t1 - Draw a visible card                       #\n"
                    "# \t2 - Draw a face-down card                     #\n"
                    "#=================================================#\n"
                )
            )
            if choice == 1:
                self.draw_from_visible_cards(visible_cards, deck, discarded_cards, False)
                visible_cards.refill_cards(discarded_cards, deck)
            else:
                self.draw_from_deck(deck)
            return

        # Draw from deck
        if choice == 2:
            self.cards.add_card(deck.draw())
            choice = int(
                input(
                    "For your 2nd card\n"
                    "#=================================================#\n"
                    "# You have the choice between the following:      #\n"
                    "# \t1 - Draw a visible card                       #\n"
                    "# \t2 - Draw a face-down card                     #\n"
                    "#=================================================#\n"
                )
            )
            if choice == 1:
                self.draw_from_visible_cards(visible_cards, deck, discarded_cards, False)
                visible_cards.refill_cards(discarded_cards, deck)

            else:
                self.draw_from_deck(deck)

        # See hand => must return to selection screen after
        if choice == 3:
            print(self.cards)
            self.draw_train_card(deck, visible_cards, discarded_cards)
            return

        # Change action
        if choice == 4:
            return self.change_str

    def place_train_pawns(self, board: Board, discarded_cards: TrainCardsDeck):
        if len(self.cards.cards) == 0:
            print("You don't have any cards in your hand now")
            return self.change_str
        roads = self.get_affordable_roads(self.get_available_roads(board))
        print(f"Here are the roads you can occupy: \n")
        i = 0
        for road in roads:
            print(f"#{i} from {road.start} to {road.end}, cost: {road.length} {road.condition} card(s) ")
            i += 1
        # only display roads that can be occupied with their costs and available resources to do it
        chosen_road_index = int(
            input(
                f"Which one do you want to occupy ? (answer expected 0 or 1 or ... or {len(roads)}) \n"
                f"\tIf you want to do another action instead type -1 \n"
                f"\tIf you want to re view the roads you can occupy type -2"
            )
        )
        if chosen_road_index == -1:
            return self.change_str

        elif chosen_road_index == -2:
            return self.place_train_pawns(board, discarded_cards)

        chosen_road = roads[chosen_road_index]
        self.pay_road_cost(chosen_road, discarded_cards)
        self.occupy_road(chosen_road)
        self.score.value += self.score.player_score_dict[chosen_road.length]

    # --- Base action
    def draw_from_deck(self, deck: TrainCardsDeck):
        card = deck.draw()
        self.cards.add_card(card)
        print(f"You drew : {card.__str__()}")

    def draw_from_visible_cards(
            self,
            visible_cards: VisibleTrainCardsDeck,
            deck: TrainCardsDeck, discarded_cards:
            TrainCardsDeck,
            first_draw: bool
    ):
        message = "Note that you can't draw a Joker on your second draw, please chose any other card \n"
        if first_draw:
            message = "Be careful, if you chose a joker you wouldn't be able to draw any more card! \n"

        print(message)

        print("Here are the visible cards :")
        i = 0
        for card in visible_cards.cards:
            i += 1
            msg = f"#{i} {card.__str__()} \n"
            print(msg)

        choice = int(
            input(
                "Chose which card you want to keep by entering its index :"
            )
        )
        if not first_draw and visible_cards.cards[choice - 1].color.value[0] == TrainCardColorEnum.JOKER.value[0]:
            print("You can't chose this card on your second draw!")
            return self.draw_from_visible_cards(visible_cards, deck, discarded_cards, False)
        index = int(choice) - 1
        chosen_card = visible_cards.get(index)
        self.cards.add_card(chosen_card)
        print(f"Added card : {chosen_card.__str__()}")
        visible_cards.refill_cards(discarded_cards, deck)

    def occupy_road(self, road: Road):
        """
        Occupy road with pawns

        :param road:
        :return:
        """
        road.occupy(self)
        # Remove pawns to occupy the road
        for _ in range(road.length):
            self.pawns.pop()

    def discard_cards(self, d_indexes: list, d_deck: TrainCardsDeck):
        for i in d_indexes:
            d_deck.add_card(self.cards.cards.pop(i))

    def pay_road_cost(self, chosen_road, d_deck: TrainCardsDeck):
        print("Choose which card you want to pay with")
        indexes = self.get_usable_card_indexes(chosen_road)
        chosen_cards_indexes = []
        for _ in range(chosen_road.length):
            print("Here are the cards you can use : ")
            self.show_cards_from_hand(indexes)
            chosen_cards_indexes.append(int(input(f"Which card do you wish to use ? \n"
                                                  f"(choose only one you will choose the rest later")))
            indexes.pop(chosen_cards_indexes[-1])
        self.discard_cards(chosen_cards_indexes, d_deck)

    def play_turn(
            self,
            board: Board,
            objective_cards_deck: ObjectiveCardsDeck,
            train_cards_deck: TrainCardsDeck,
            visible_train_cards_deck: VisibleTrainCardsDeck,
            discarded_train_cards: TrainCardsDeck
    ):
        """
        Do the turn of the player

        :return:
        """
        choice = int(
            input(
                "#=================================================#\n"
                "# You have the choice between the following:      #\n"
                "# \t1 - Draw a train card                         #\n"
                "# \t2 - Draw an Objective card                    #\n"
                "# \t3 - Occupy a road                             #\n"
                "# \t4 - View your Train Cards                     #\n"
                "# \t5 - View your Objective Cards                 #\n"
                "#=================================================#\n"
            )
        )

        if choice == 1:
            c = self.draw_train_card(train_cards_deck, visible_train_cards_deck, discarded_train_cards)
            if c == self.change_str:
                return self.play_turn(
                    board,
                    objective_cards_deck,
                    train_cards_deck,
                    visible_train_cards_deck,
                    discarded_train_cards
                )
        elif choice == 2:
            c = self.draw_objective_card(objective_cards_deck)
            if c == self.change_str:
                return self.play_turn(
                    board,
                    objective_cards_deck,
                    train_cards_deck,
                    visible_train_cards_deck,
                    discarded_train_cards
                )
        elif choice == 3:
            c = self.place_train_pawns(board, discarded_train_cards)
            if c == self.change_str:
                return self.play_turn(
                    board,
                    objective_cards_deck,
                    train_cards_deck,
                    visible_train_cards_deck,
                    discarded_train_cards
                )
        elif choice == 4:
            self.show_cards_from_hand("all")
        elif choice == 5:
            self.show_objective_cards()

    # --- Utils
    @staticmethod
    def get_available_roads(board: Board):
        available_roads = []
        for road in board.roads:
            if not road.occupied:
                available_roads.append(road)
        return available_roads

    def get_affordable_roads(self, available_roads: list):
        hand = self.cards.count_by_color()
        affordable_roads = []
        for road in available_roads:
            if road.condition is not None:
                if road.condition.value[0] in hand.keys() and hand[road.condition.value[0]] >= road.length:
                    affordable_roads.append(road)

            else:
                if sum(hand.values()):
                    affordable_roads.append(road)
        return affordable_roads

    def get_usable_card_indexes(self, color_cost: Road):
        index = 0
        usable_card_indexes = []
        if color_cost.condition is None:
            usable_card_indexes = [i for i in range(len(self.cards.cards))]
        else:
            for card in self.cards.cards:
                if card.color == color_cost.condition:
                    usable_card_indexes.append(index)
                index += 1
        return usable_card_indexes

    def show_cards_from_hand(self, indexes):
        c = 0
        if indexes == "all":
            indexes = [i for i in range(len(self.cards.cards))]
            if len(indexes) == 0:
                print(f"You don't have any cards now")
                return
        for index in indexes:
            print(f"#{c} {self.cards.cards[index]}")
            c += 1

    def show_objective_cards(self):
        c = 0
        print("Here are your objective cards")
        for card in self.objectives.cards:
            c += 1
            print(f"\t#{c} , {card}")

    def show_visible_card(self, visible_cards: TrainCardsDeck):
        index = 0
        print("Here are the visible cards")
        for card in visible_cards.cards:
            index += 1
            print(f"#\t {index} , {card.__str__()}")

    # --- Operators

    def __str__(self):
        return f"Player #{self.turn_order} ({self.str_type}) color : {self.color.value}"

    def __lt__(self, other):
        if self.score.value == other.score.value:
            # First sort
            if self.score.value == 0:
                return self.turn_order < other.turn_order

            if self.completed_objectives_count == other.completed_objectives_count:
                return Algorithm.longest_road(self) < Algorithm.longest_road(other)

            return self.completed_objectives_count < other.completed_objectives_count

        return self.score.value < other.score.value

    def __gt__(self, other):
        if self.score.value == other.score.value:
            # First sort
            if self.score.value == 0:
                return self.turn_order > other.turn_order

            if self.completed_objectives_count == other.completed_objectives_count:
                return Algorithm.longest_road(self) > Algorithm.longest_road(other)

            return self.completed_objectives_count > other.completed_objectives_count

        return self.score.value > other.score.value

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        return self.__ge__(other) and self.__le__(other)


class AIPlayer(Player):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "AI"

    def draw_objective_card(self, source: ObjectiveCardsDeck, first_turn=False):
        drawn_cards = [source.draw() for _ in range(3)]

        # Logic to keep cards based on some heuristic
        kept_cards = random.sample(drawn_cards, k=2 if first_turn else 1)
        discarded_cards = [card for card in drawn_cards if card not in kept_cards]

        self.objectives.cards.extend(kept_cards)
        source.cards.extend(discarded_cards)

    def draw_train_card(self, deck: TrainCardsDeck, visible_cards: VisibleTrainCardsDeck,
                        discarded_cards: TrainCardsDeck):
        # Example heuristic: prioritize non-joker visible cards, then face-down cards
        if visible_cards.cards:
            non_joker_cards = [card for card in visible_cards.cards if card.color != TrainCardColorEnum.JOKER]
            if non_joker_cards:
                chosen_card = random.choice(non_joker_cards)
                self.cards.add_card(chosen_card)
                visible_cards.cards.remove(chosen_card)
            else:
                self.cards.add_card(deck.draw())
        else:
            self.cards.add_card(deck.draw())

        visible_cards.refill_cards(discarded_cards, deck)

        if visible_cards.cards:
            non_joker_cards = [card for card in visible_cards.cards if card.color != TrainCardColorEnum.JOKER]
            if non_joker_cards:
                chosen_card = random.choice(non_joker_cards)
                self.cards.add_card(chosen_card)
                visible_cards.cards.remove(chosen_card)
            else:
                self.cards.add_card(deck.draw())
        else:
            self.cards.add_card(deck.draw())

        visible_cards.refill_cards(discarded_cards, deck)

    def place_train_pawns(self, board: Board, discarded_cards: TrainCardsDeck):
        available_roads = self.get_affordable_roads(self.get_available_roads(board))

        if available_roads:
            chosen_road = random.choice(available_roads)
            self.pay_road_cost(chosen_road, discarded_cards)
            self.occupy_road(chosen_road)
            self.score.value += self.score.player_score_dict[chosen_road.length]
        else:
            return self.change_str

    def play_turn(self, board: Board, objective_cards_deck: ObjectiveCardsDeck, train_cards_deck: TrainCardsDeck,
                  visible_train_cards_deck: VisibleTrainCardsDeck, discarded_train_cards: TrainCardsDeck):
        choice = random.choice([1, 2, 3])
        if choice == 1:
            self.draw_train_card(train_cards_deck, visible_train_cards_deck, discarded_train_cards)
        elif choice == 2:
            self.draw_objective_card(objective_cards_deck)
        elif choice == 3:
            c = self.place_train_pawns(board, discarded_train_cards)
            if c == self.change_str:
                return self.play_turn(board, objective_cards_deck, train_cards_deck, visible_train_cards_deck,
                                      discarded_train_cards)
        else:
            return self.play_turn(board, objective_cards_deck, train_cards_deck, visible_train_cards_deck,
                                  discarded_train_cards)

    def draw_from_visible_cards(self, visible_cards: VisibleTrainCardsDeck, deck: TrainCardsDeck,
                                discarded_cards: TrainCardsDeck, first_draw: bool):
        if visible_cards.cards:
            non_joker_cards = [card for card in visible_cards.cards if card.color != TrainCardColorEnum.JOKER]
            if first_draw or not non_joker_cards:
                chosen_card = random.choice(visible_cards.cards)
            else:
                chosen_card = random.choice(non_joker_cards)

            self.cards.add_card(chosen_card)
            visible_cards.cards.remove(chosen_card)
            visible_cards.refill_cards(discarded_cards, deck)
        else:
            self.cards.add_card(deck.draw())

    def pay_road_cost(self, chosen_road: Road, discarded_cards: TrainCardsDeck):
        usable_cards = self.get_usable_card_indexes(chosen_road)
        chosen_cards = random.sample(usable_cards, k=chosen_road.length)
        self.discard_cards(chosen_cards, discarded_cards)


class RandomAIPlayer(AIPlayer):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "Random AI"


class GreedyAIPlayer(AIPlayer):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "Greedy AI"

    def draw_objective_card(self, source: ObjectiveCardsDeck, first_turn=False):
        drawn_cards = [source.draw() for _ in range(3)]

        # Keep the cards with the highest points
        drawn_cards.sort(key=lambda card: card.points, reverse=True)
        kept_cards = drawn_cards[:2 if first_turn else 1]
        discarded_cards = drawn_cards[2 if first_turn else 1:]

        self.objectives.cards.extend(kept_cards)
        source.cards.extend(discarded_cards)

    def draw_train_card(self, deck: TrainCardsDeck, visible_cards: VisibleTrainCardsDeck,
                        discarded_cards: TrainCardsDeck):
        # Prioritize drawing visible non-joker cards, then draw from deck
        non_joker_cards = [card for card in visible_cards.cards if card.color != TrainCardColorEnum.JOKER]
        if non_joker_cards:
            chosen_card = max(non_joker_cards, key=lambda card: card.points)  # Or some other metric
            self.cards.add_card(chosen_card)
            visible_cards.cards.remove(chosen_card)
        else:
            self.cards.add_card(deck.draw())

        visible_cards.refill_cards(discarded_cards, deck)

        if visible_cards.cards:
            non_joker_cards = [card for card in visible_cards.cards if card.color != TrainCardColorEnum.JOKER]
            if non_joker_cards:
                chosen_card = max(non_joker_cards, key=lambda card: card.points)  # Or some other metric
                self.cards.add_card(chosen_card)
                visible_cards.cards.remove(chosen_card)
            else:
                self.cards.add_card(deck.draw())
        else:
            self.cards.add_card(deck.draw())

        visible_cards.refill_cards(discarded_cards, deck)


class DefensiveAIPlayer(AIPlayer):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "Defensive AI"

    def place_train_pawns(self, board: Board, discarded_cards: TrainCardsDeck):
        available_roads = self.get_affordable_roads(self.get_available_roads(board))

        if available_roads:
            # Choose roads strategically to block opponents
            chosen_road = self.choose_blocking_road(available_roads)
            self.pay_road_cost(chosen_road, discarded_cards)
            self.occupy_road(chosen_road)
            self.score.value += self.score.player_score_dict[chosen_road.length]
        else:
            return self.change_str

    def choose_blocking_road(self, available_roads: list):
        # Implement logic to choose a road that would block opponents
        # For simplicity, we randomly choose a road
        return random.choice(available_roads)


class BalancedAIPlayer(AIPlayer):
    def __init__(self, _color: PlayerColorEnum, _turn_order: int):
        super().__init__(_color, _turn_order)
        self.str_type = "Balanced AI"

    def play_turn(self, board: Board, objective_cards_deck: ObjectiveCardsDeck, train_cards_deck: TrainCardsDeck,
                  visible_train_cards_deck: VisibleTrainCardsDeck, discarded_train_cards: TrainCardsDeck):
        # Balance between drawing cards, drawing objectives, and occupying roads
        choices = [1, 2, 3]
        choice = random.choice(choices)

        if choice == 1:
            self.draw_train_card(train_cards_deck, visible_train_cards_deck, discarded_train_cards)
        elif choice == 2:
            self.draw_objective_card(objective_cards_deck)
        elif choice == 3:
            c = self.place_train_pawns(board, discarded_train_cards)
            if c == self.change_str:
                return self.play_turn(board, objective_cards_deck, train_cards_deck, visible_train_cards_deck,
                                      discarded_train_cards)
        else:
            return self.play_turn(board, objective_cards_deck, train_cards_deck, visible_train_cards_deck,
                                  discarded_train_cards)
