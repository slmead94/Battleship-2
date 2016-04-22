"""
//------------------------------------------------------------------//
                        *--Battleship 2--*
//******************************************************************//

Spencer M.
Assignment: Final Project
Semester 2, Freshman Year HS
Started: April 20th, 11:30, 2016

//******************************************************************//

"""
import util


def intro():
    print "\tWelcome to Battleship 2!\n"


def get_baseline():
    intro()
    chosen_level = None
    chosen_type = None
    more = True
    continue_ = True
    battlefield_types = [[10, 10], [15, 15], [20, 20]]  # 10 X 10, 15 X 15, 20 X 20
    game_modes = ["Lieutenant", "Captain", "Admiral"]  # different Naval Ranks for the skill levels
    name = raw_input("Enter your name: ")  # name please?

    print "\nYou may choose from " + str(len(battlefield_types)) + " different battlefield types:\n"
    for i in range(0, len(battlefield_types)):
        print str(i + 1) + ".   " + str(battlefield_types[i][0]) + " X " + str(battlefield_types[i][1])  # print list in format
    while more:  # verification loop
        chosen_type = raw_input("Choose one of the above numbers: ")
        more = util.try_int(chosen_type, [1, 2, 3])

    print "\nYou may choose from " + str(len(game_modes)) + " game modes to play:\n"
    for j in range(0, len(game_modes)):
        print str(j + 1) + ".  " + game_modes[j]  # print list in format
    while continue_:
        chosen_level = raw_input("Choose one of the above numbers: ")
        continue_ = util.try_int(chosen_level, [1, 2, 3])

    # fill variables with the data we have just collected:
    width = battlefield_types[int(chosen_type) - 1][0]
    height = battlefield_types[int(chosen_type) - 1][1]
    mode = game_modes[int(chosen_level) - 1]

    new_player = Player(mode, name)
    new_board = Battlefield(height, width, "Player Board")
    new_board.fill_board()  # fill the new board with all empty spaces

    return new_board, new_player  # return the new objects to be used in Main


class Player:
    def __init__(self, game_mode, name="Computer"):
        self.name = name
        self.game_mode = game_mode
        self.winner = False
        self.number_hits = 0
        self.number_sunk = 0


class Battlefield:
    def __init__(self, height, width, header):
        self.header = header
        self.height = height
        self.width = width
        self.empty = "_"
        self.ship_up = "^"
        self.ship_down = "V"
        self.ship_left = "<"
        self.ship_right = ">"
        self.main_board = []
        self.board_numbers = []

    def fill_board(self):
        for i in range(0, self.height):
            self.main_board.append([])  # append a row
            self.board_numbers.append(str(i + 1))  # append to the top row of numbers
            for j in range(0, self.width):
                self.main_board[i].append(self.empty)


class Screen:
    def __init__(self):
        self.spacer = "| "
        self.other_line = "    ___________________________________________________________"

    def print_board(self, board_object):
        print board_object.header
        print "    ",
        for i in range(0, len(board_object.board_numbers)):  # print the numbers
            if i < 9:  # if the number is double digits take away one space to keep it even
                print board_object.board_numbers[i] + "  ",
            else:
                print board_object.board_numbers[i] + " ",
        print  # space

        print self.other_line
        for rows in range(0, board_object.height):
            if rows < 9:  # if the number is double digit take away 1 space
                print str(rows + 1) + " ",
            else:
                print str(rows + 1),
            for columns in range(0, board_object.width):
                print self.spacer + board_object.main_board[rows][columns],
            print self.spacer


class Main:
    def __init__(self, user, battlefield):
        self.battlefield = battlefield
        self.user = user

player_board, player = get_baseline()
main_game = Main(player, player_board)
