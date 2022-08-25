import random
import time


class Game:
    def __init__(self):
        self.vertical_x_o = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]
        self.horizontal_x_o = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]
        self.board_options = [(0, 0), (1, 0), (2, 0),
                              (0, 1), (1, 1), (2, 1),
                              (0, 2), (1, 2), (2, 2)]

        self.STATUS = 0
        self.odd_or_even = ""

    def my_turn(self, choice):
        if self.vertical_x_o[choice[1]][choice[0]] == 9:
            self.board_options.remove(choice)
            self.vertical_x_o[choice[1]][choice[0]] = 0
            self.horizontal_x_o[choice[0]][choice[1]] = 0
            if self.check_if_win(self.vertical_x_o) or self.check_if_win(self.horizontal_x_o):
                return "win"

    def get_opponent_choice(self):
        if len(self.board_options) > 0:
            opponent_choice = random.choice(self.board_options)
            self.board_options.remove(opponent_choice)
            return opponent_choice
        else:
            return "last_move"

    def opponent_turn(self, opponent_choice):

        time.sleep(0.5)

        if opponent_choice != "last_move":
            self.vertical_x_o[opponent_choice[1]][opponent_choice[0]] = 1
            self.horizontal_x_o[opponent_choice[0]][opponent_choice[1]] = 1
            if self.check_if_win(self.vertical_x_o) == False \
                    or self.check_if_win(self.horizontal_x_o) == False:
                return "lose"

    def check_if_win(self, seq):
        for i in seq:
            print(i)
            if sum(i) == 0:
                return True
            if sum(i) == 3:
                return False

        diagonal_1 = seq[0][0] + seq[1][1] + seq[2][2]
        diagonal_2 = seq[0][2] + seq[1][1] + seq[2][0]

        if diagonal_1 == 0 or diagonal_2 == 0:
            return True
        if diagonal_1 == 3 or diagonal_2 == 3:
            return False

    def check_if_game_ends_in_tie(self):
        if len(self.board_options) == 0 \
                and self.check_if_win(self.vertical_x_o) == None \
                and self.check_if_win(self.horizontal_x_o) == None:
            return True

    def check_if_lose(self, seq):
        for i in seq:
            print(i)
            if sum(i) == 3:
                return True

    def restart(self):
        self.__init__()
