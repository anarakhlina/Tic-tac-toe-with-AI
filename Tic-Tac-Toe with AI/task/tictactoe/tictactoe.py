# write your code here
import copy
import math
import random
from math import inf

HUMAN = -1
COMP = +1

class TicTacToeGame:
    def __init__(self, players, field_config="_________"):
        self.size = round(math.sqrt(len(field_config)))
        self.field = []
        for i in range(self.size):
            field_row = []
            for j in range(self.size):
                field_row.append(field_config[i * self.size + j])
            self.field.append(field_row)
        self.players = players
        self.x_quan = self.count(self.field, "X")
        self.o_quan = self.count(self.field, "O")
        self.free = [[i, j] for j in range(0, self.size) for i in range(0, self.size) if self.field[i][j] == "_"]

    def count(self, field, el):
        quan = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if field[i][j] == el:
                    quan += 1
        return quan

    def print_field(self):
        print("---------")
        for i in range(self.size):
            print("|", end="")
            for j in range(self.size):
                if self.field[i][j] == "_":
                    print("  ", end=""),
                else:
                    print(" " + self.field[i][j], end=""),
            print(" |")
        print("---------")

    def game_state(self, field):
        win_conditions = [field[i] for i in range(self.size)]  # 3 in a row
        for j in range(self.size):
            win_conditions.append([field[i][j] for i in range(self.size)])  # 3 in a col
        win_conditions.append([field[i][i] for i in range(self.size)])  # main diagonal
        win_conditions.append([field[i][self.size - i - 1] for i in range(self.size)])  # reverse diagonal
        if list("X" * self.size) in win_conditions:
            return "X wins"
        elif list("O" * self.size) in win_conditions:
            return "O wins"
        count_free = self.count(field, "_")
        if count_free == 0:
            return "Draw"
        return "Game not finished"

    def make_move(self, coord, symbol):
        if coord[0] < 0 or coord[0] > 2 or coord[1] < 0 or coord[1] > 2:
            print("Coordinates should be from 1 to 3!")
            return 0
        if self.field[coord[0]][coord[1]] != "_":
            print("This cell is occupied! Choose another one!")
            return 0
        fieldcopy = copy.deepcopy(self.field)
        fieldcopy[coord[0]][coord[1]] = symbol
        return fieldcopy

    def user_plays(self, symbol):
        while True:
            coord = input("Enter the coordinates:").split()
            if coord[0] == "exit":
                return 0
            if not all(map(str.isnumeric, coord)):
                print("You should enter numbers!")
            else:
                cor = int(coord[0]) - 1
                coord[0] = self.size - int(coord[1])
                coord[1] = cor
                new_field = self.make_move(coord, symbol)
                if new_field != 0:
                    self.field = new_field
                    self.free.remove([coord[0], coord[1]])
                    break;
        if symbol == "X":
            self.x_quan += 1
        else:
            self.o_quan += 1
        return 1

    def easyAI_plays(self, symbol):
        print('Making move level "easy"')
        coord = random.choice(self.free)
        self.field = self.make_move(coord, symbol)
        self.free.remove(coord)
        if symbol == "X":
            self.x_quan += 1
        else:
            self.o_quan += 1
        return 1

    def mediumAI_plays(self, symbol):
        print('Making move level "medium"')
        if symbol == "X":
            opponent_symbol = "O"
        else:
            opponent_symbol = "X"
        coord = -1
        for i in range(self.size):
            if self.field[i].count(symbol) == self.size - 1:
                try:
                    coord = [i, self.field[i].index("_")]
                    break
                except ValueError:
                    coord = -1
            elif self.field[i].count(opponent_symbol) == self.size - 1:
                try:
                    coord = [i, self.field[i].index("_")]
                    break
                except ValueError:
                    coord = -1
            else:
                column_check = [self.field[j][i] for j in range(self.size)]
                if column_check.count(symbol) == self.size - 1:
                    try:
                        coord = [column_check.index("_"), i]
                        break
                    except ValueError:
                        coord = -1
                if column_check.count(opponent_symbol) == self.size - 1:
                    try:
                        coord = [column_check.index("_"), i]
                        break
                    except ValueError:
                        coord = -1
        if coord == -1:
            coord = random.choice(self.free)
        self.field = self.make_move(coord, symbol)
        self.free.remove(coord)
        if symbol == "X":
            self.x_quan += 1
        else:
            self.o_quan += 1
        return 1

    def minimax(self, depth, player, symbol):
        if player == COMP:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]

        if symbol == "X":
            opponent_symbol = "O"
        else:
            opponent_symbol = "X"

        if depth == 0 or self.game_state(self.field) != "Game not finished":
            state = self.game_state(self.field)
            if state == "Draw":
                return [-1, -1, 0]
            elif player == COMP:
                if state == symbol + " wins":
                    return [-1, -1, 1]
                else:
                    return [-1, -1, -1]
            elif player == HUMAN:
                if state == symbol + " wins":
                    return [-1, -1, -1]
                else:
                    return [-1, -1, 1]

        for cell in self.free:
            x, y = cell[0], cell[1]
            self.field[x][y] = symbol
            self.free.remove([x, y])
            score = self.minimax(depth - 1, -player, opponent_symbol)
            self.free.append([x, y])
            self.field[x][y] = "_"
            score[0], score[1] = x, y

            if player == COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def hardAI_plays(self, symbol):
        depth = len(self.free)
        if depth == 0:
            return
        print('Making move level "hard"')
        if depth == math.pow(self.size, 2):
            coord = random.choice(self.free)
            self.field = self.make_move(coord, symbol)
            self.free.remove(coord)
            if symbol == "X":
                self.x_quan += 1
            else:
                self.o_quan += 1
            return 1
        else:
            coord = self.minimax(depth, COMP, symbol)
            coord = [coord[0], coord[1]]
        self.field = self.make_move(coord, symbol)
        self.free.remove(coord)
        if symbol == "X":
            self.x_quan += 1
        else:
            self.o_quan += 1
        return 1

    def who_plays(self, player, symbol):
        if player == "user":
            return self.user_plays(symbol)
        elif player == "easy":
            return self.easyAI_plays(symbol)
        elif player == "medium":
            return self.mediumAI_plays(symbol)
        elif player == "hard":
            return self.hardAI_plays(symbol)

    def game_play(self):
        self.print_field()
        while self.game_state(self.field) == "Game not finished":
            if self.x_quan == self.o_quan:
                if not self.who_plays(self.players[0], "X"):
                    return 0
            else:
                if not self.who_plays(self.players[1], "O"):
                    return 0
            self.print_field()
        print(self.game_state(self.field))
        return 1


while True:
    print("Input command:")
    command = input().split()
    if command[0] == "exit":
        break
    if len(command) != 3:
        print("Bad parameters")
    else:
        command.remove("start")
        tictactoe = TicTacToeGame(command)
        if tictactoe.game_play() == 0:
            break