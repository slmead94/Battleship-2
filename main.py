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


def get_baseline():
    print "\tWelcome to Battleship 2!\n"
    chosen_level = None
    chosen_type = None
    more = True
    continue_ = True
    battlefield_types = [[10, 10], [15, 15], [20, 20]]  # 10 X 10, 15 X 15, 20 X 20
    game_modes = ["Lieutenant", "Captain", "Admiral"]  # different Naval Ranks for the skill levels
    name = raw_input("Enter your name: ")  # name please?

    print "\nYou may choose from " + str(len(battlefield_types)) + " different battlefield types: (less space - easier to hit each other)\n"
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

    # create objects to return
    p_fleet = Fleet("User")
    c_fleet = Fleet("Computer")
    new_player = Player(mode, name)
    comp_player = Player(mode, "Computer")
    new_board = Battlefield(height, width, "Player Board")
    comp_board = Battlefield(height, width, "Computer Board")
    new_board.fill_board()  # fill the new board with all empty spaces

    return new_board, new_player, comp_board, comp_player, p_fleet, c_fleet  # return the new objects to be used in Main


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

    @staticmethod
    def add_ship(ship):
        print ship


class Screen:
    def __init__(self):
        self.spacer = "| "
        self.other_line = ""

    def intro_board(self):
        print "\nThis is what the board looks like:\n"
        self.print_board(main_game.battlefield)
        raw_input("\nPress Return: ")  # pause the program so the user can keep up
        print "\nYou will place your ships and fire at the opponents ships by\n" \
              "choosing an x and y coordinate (with the addition of choosing a direction when you place your ships).\n"

    def print_board(self, board_object):
        i = 0

        print board_object.header
        print "    ",
        for i in range(0, len(board_object.board_numbers)):  # print the numbers
            if i < 9:  # if the number is double digits take away one space to keep it even
                print board_object.board_numbers[i] + "  ",
            else:
                print board_object.board_numbers[i] + " ",
        self.other_line = "    " + "____" * (i + 1)
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


class Fleet:
    def __init__(self, who):
        self.ship_lengths = [5, 4, 3, 3, 2]
        self.directions = ["Up", "Down", "Left", "Right"]
        self.names = ["Carrier", "Battleship", "Cruiser", "Submarine", "Frigate"]
        self.ships = []  # list of 5 ship objects
        self.destroyed = False
        self.num_ships = len(self.names)
        self.who = who

        self.total_lengths = 0  # calculate the total lengths of all of the ships
        for i in range(0, len(self.ship_lengths)):
            self.total_lengths += self.ship_lengths[i]

    def make_ships(self):
        direct = None
        x_axis = None
        y_axis = None

        for i in range(len(self.ship_lengths)):
            # boolean loop controllers:
            more = True
            mores = True
            more_ = True

            print self.names[i] + ":\n"
            for j in range(len(self.directions)):  # print the list of directions to chose from
                print str(j + 1) + ".  " + self.directions[j]
            print  # spacer

            while more:  # get direction
                direct = raw_input("Choose the number related to the direction that you would like your " + self.names[i] + " to face: ")
                more = util.try_int(direct, [1, 2, 3, 4])
            direct = self.directions[int(direct) - 1][0]

            x_list, y_list = self.get_list(direct, i)
            print x_list
            print y_list

            # pre-made messages because they are too long to fit inside of a raw_input() statement and still be behind the line:
            txt_width = "Choose an X coordinate for your " + self.names[i] + "'s head to be on (" + x_list[0] + " - " + x_list[-1] + "): "
            txt_height = "Choose an Y coordinate for your " + self.names[i] + "'s head to be on (" + y_list[0] + " - " + y_list[-1] + "): "

            while mores:  # get x coordinate
                x_axis = raw_input(txt_width)
                mores = util.try_battlefield_int(x_axis, x_list)

            while more_:  # get y coordinate
                y_axis = raw_input(txt_height)
                more_ = util.try_battlefield_int(y_axis, y_list)

            new_ship = Ship(self.ship_lengths[i], self.names[i], direct, x_axis, y_axis)
            self.ships.append(new_ship)  # append the newest ship to the ships list
            player_board.add_ship(new_ship)  # put newly create ship on the board
            print  # spacer

    def get_list(self, direction, counter):
        """

        :param direction: The direction the boat wants be pointed in
        :param counter: the current value of i in the method that called this method

        :return: newly made lists for use back in the ship creation method

        I originally had an if statement for each direction but I realized that
        a couple of them had very very similar features and decided to combine them.
        To do so I had to add a few more variables and a couple more if / elif statements
        at the bottom of the method, but it works a whole lot more efficiently now.
        """

        x_axis_ls = []
        y_axis_ls = []
        count_x = player_board.width
        count_y = player_board.height
        beg_y = 0
        beg_x = 0
        var = 0
        chosen = 0
        chosen_ = 0

        if player_board.width == 10:
            var = 0
        elif player_board.width == 15:
            var = 5
        elif player_board.width == 20:
            var = 10

        if direction == "U" or direction == "L":
            if self.ship_lengths[counter] == 5:
                chosen = 6 + var
            elif self.ship_lengths[counter] == 4:
                chosen = 7 + var
            elif self.ship_lengths[counter] == 3:
                chosen = 8 + var
            elif self.ship_lengths[counter] == 2:
                chosen = 9 + var
        elif direction == "D" or direction == "R":
            if self.ship_lengths[counter] == 5:
                chosen_ = 4
            elif self.ship_lengths[counter] == 4:
                chosen_ = 3
            elif self.ship_lengths[counter] == 3:
                chosen_ = 2
            elif self.ship_lengths[counter] == 2:
                chosen_ = 1

        if direction == "U":
            count_y = chosen
        elif direction == "L":
            count_x = chosen
        elif direction == "D":
            beg_y = chosen_
        elif direction == "R":
            beg_x = chosen_

        for j in range(beg_y, count_y):
            y_axis_ls.append(str(j + 1))
        for i in range(beg_x, count_x):
            x_axis_ls.append(str(i + 1))

        return x_axis_ls, y_axis_ls


class Ship:
    def __init__(self, length, ship_name, direction, x, y):
        self.length = length
        self.direction = direction
        self.ship_name = ship_name
        self.x = x
        self.y = y
        self.sunk = False


class Player:
    def __init__(self, game_mode, name="Computer"):
        self.name = name
        self.game_mode = game_mode
        self.winner = False

        # stats:
        self.number_hits = 0
        self.number_sunk = 0
        self.shots_fired = 0
        self.number_missed = 0


class Main:
    def __init__(self, user, battlefield, comp_battlefield, comp):
        self.battlefield = battlefield
        self.user = user
        self.comp = comp
        self.computer_board = comp_battlefield

player_board, player, computer_board, computer, player_fleet, comp_fleet = get_baseline()  # start program and get basic information

main_game = Main(player, player_board, computer_board, computer)  # create the main object
screen = Screen()
screen.intro_board()
player_fleet.make_ships()
