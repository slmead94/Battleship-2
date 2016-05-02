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
import random


def get_baseline():
    chosen_level = None
    chosen_type = None
    more = True
    continue_ = True
    battlefield_types = [[10, 10], [15, 15], [20, 20]]  # 10 X 10, 15 X 15, 20 X 20
    game_modes = ["Lieutenant", "Captain", "Admiral"]  # different Naval Ranks for the skill levels

    print "\tWelcome to Battleship 2!\n"
    name = raw_input("Enter your name: ")  # name please?

    print "\nYou may choose from " + str(len(battlefield_types)) + " different battlefield types: (less space - easier to hit each other)\n"
    for i in range(0, len(battlefield_types)):
        print str(i + 1) + ".   " + str(battlefield_types[i][0]) + " X " + str(battlefield_types[i][1])  # print list in format

    while more:  # verification loop
        chosen_type = raw_input("Choose one of the above numbers: ")
        more = util.try_int(chosen_type, [1, 2, 3])

    print "\nYou may choose from " + str(len(game_modes)) + " different game modes to play:\n"
    screen.print_numbered_list(game_modes)

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
    new_board.fill_board()  # fill the new board with all empty spaces
    comp_board = Battlefield(height, width, "Computer Board")
    comp_board.fill_board()  # fill the new computer board with empty spaces

    return new_board, new_player, comp_board, comp_player, p_fleet, c_fleet  # return the new objects to be used in Main


class Battlefield:
    def __init__(self, height, width, header):
        self.header = header
        self.height = height
        self.width = width
        self.empty = "_"
        self.ship_types = ["V", "<", ">", "^"]
        self.ship_up = "^"
        self.ship_down = "V"
        self.ship_left = "<"
        self.ship_right = ">"
        self.hit = "X"
        self.miss = "*"
        self.main_board = []
        self.board_numbers = []

    def fill_board(self):
        for i in range(0, self.height):
            self.main_board.append([])  # append a row
            self.board_numbers.append(str(i + 1))  # append to the top row of numbers
            for j in range(0, self.width):
                self.main_board[i].append(self.empty)

    def fire(self, x, y, who):
        x_axis = int(x) - 1  # decrement the variables so they can work correctly with lists
        y_axis = int(y) - 1

        if who.upper() == "USER":
            if computer_board.main_board[y_axis][x_axis] in self.ship_types:
                print "You have hit a ship!\n"
                computer_board.main_board[y_axis][x_axis] = self.hit
                player.number_hits += 1

            elif computer_board.main_board[y_axis][x_axis] == self.empty:
                print "Miss\n"
                computer_board.main_board[y_axis][x_axis] = self.miss
                player.number_missed += 1

            player.shots_fired += 1
        else:
            if player_board.main_board[y_axis][x_axis] in self.ship_types:
                print "You have been hit!!!\n"
                player_board.main_board[y_axis][x_axis] = self.hit
                computer.number_hits += 1

            elif player_board.main_board[y_axis][x_axis] == self.empty:
                print "The computer missed you\n"
                player_board.main_board[y_axis][x_axis] = self.miss
                computer.number_missed += 1

            computer.shots_fired += 1
            screen.print_board(player_board)

    def add_ship(self, ship, board):
        # we have to decrement the coordinates so they conform to the ways of the list
        ship.y = int(ship.y) - 1
        ship.x = int(ship.x) - 1

        if ship.direction == "U":
            symbol = self.ship_up
            for i in range(0, ship.length):
                board.main_board[ship.y + i][ship.x] = symbol

        elif ship.direction == "D":
            symbol = self.ship_down
            for i in range(0, ship.length):
                    board.main_board[ship.y - i][ship.x] = symbol

        elif ship.direction == "L":
            symbol = self.ship_left
            for i in range(0, ship.length):
                board.main_board[ship.y][ship.x + i] = symbol

        elif ship.direction == "R":
            symbol = self.ship_right
            for i in range(0, ship.length):
                board.main_board[ship.y][ship.x - i] = symbol

        if board.header == "Player Board":
            print
            screen.print_board(board)


class Screen:
    def __init__(self):
        self.spacer = "| "
        self.other_line = ""

    def intro_board(self):
        print "\nThis is what the board looks like:\n"
        self.print_board(player_board)
        raw_input("\nPress Return: ")  # pause the program so the user can keep up
        print "\nYou will place your ships and fire at the opponents ships by\n" \
              "choosing an x and y coordinate (with the addition of choosing a direction when you place your ships).\n"

    @staticmethod
    def battle_intro():
        print "\nYou will fire at the opponent by choosing an X and Y coordinate."

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

    @staticmethod
    def print_numbered_list(ls):
        # this makes printing a list with numbers in front of each item much more accessible
        for i in range(0, len(ls)):
            print str(i + 1) + ".  " + ls[i]
        print


class Fleet:
    def __init__(self, who):
        self.ship_lengths = [5, 4, 3, 3, 2]
        self.directions = ["Up", "Down", "Left", "Right"]
        self.names = ["Carrier", "Battleship", "Cruiser", "Submarine", "Frigate"]
        self.ships = []  # list of 5 ship objects
        self.destroyed = False
        self.num_ships = len(self.names)
        self.who = who
        self.total_lengths = 0

        # Calculate the total lengths of all of the ships:
        # This is here in case we decide to change the length of a ship later.
        # It makes it more susceptible to change in the future.
        for i in range(0, len(self.ship_lengths)):
            self.total_lengths += self.ship_lengths[i]

    def make_comp_ships(self):
        used_x_axis = []
        used_y_axis = []
        for i in range(0, len(self.ship_lengths)):
            x_axis = None
            y_axis = None
            more = True
            more_ = True
            direct = "U"  # as of now the computer's ships will all be facing upwards
            x_list, y_list = self.get_list(direct, i)

            while more:
                x_axis = random.choice(x_list)
                more = util.try_computer_ship_coordinate(x_axis, used_x_axis)
            used_x_axis.append(x_axis)
            x_axis = int(x_axis)

            while more_:
                y_axis = random.choice(y_list)
                more_ = util.try_computer_ship_coordinate(y_axis, used_y_axis)
            used_y_axis.append(y_axis)
            y_axis = int(y_axis)

            new_ship = Ship(self.ship_lengths[i], "Computer's " + self.names[i], direct, x_axis, y_axis)
            self.ships.append(new_ship)
            computer_board.add_ship(new_ship, computer_board)

    def make_ships(self):
        direct = None
        x_axis = None
        y_axis = None

        for i in range(len(self.ship_lengths)):
            # boolean loop controllers:
            more = True
            mores = True
            more_ = True

            print self.names[i] + " (size=" + str(self.ship_lengths[i]) + "):\n"
            screen.print_numbered_list(self.directions)

            while more:  # get direction
                direct = raw_input("Choose the number related to the direction that you would like your " + self.names[i] + " to face: ")
                more = util.try_int(direct, [1, 2, 3, 4])
            direct = self.directions[int(direct) - 1][0]

            x_list, y_list = self.get_list(direct, i)
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
            player_board.add_ship(new_ship, player_board)  # put newly create ship on the board
            print  # spacer

    def get_list(self, direction, counter):
        """

        :param direction: The direction the boat wants be pointed in
        :param counter: the current value of i in the method that called this method
        :return: newly made lists for use back in the ship creation method ^^

        This method creates a list with the correct values depending on the size
        of the battlefield and then returns it so the user is forced to choose
        certain rows and columns so the ships don't automatically overlap.

        I originally had an if statement for each direction but I realized that
        a couple of them had very very similar features and decided to combine them.
        To do so I had to add a few more variables and a couple more if / elif statements
        at the bottom of the method, but it works a whole lot more efficiently now.
        """

        x_axis_ls = []
        y_axis_ls = []
        count_x = player_board.width  # the player board is the same dimensions as the computer's board
        count_y = player_board.height
        beg_y = 0
        beg_x = 0
        var = 0
        chosen = 0
        chosen_ = 0

        # this determines how much to add to the original hard coded values in the below algorithm
        if player_board.width == 10:
            var = 0
        elif player_board.width == 15:
            var = 5
        elif player_board.width == 20:
            var = 10

        if direction == "U" or direction == "L":
            # the values like 6, 7, 8, etc. would need to be edited if we ever changed the length of a ship
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


class Player:
    def __init__(self, game_mode, name="Computer"):
        self.name = name
        self.game_mode = game_mode
        self.winner = False

        # stats:
        self.number_missed = 0
        self.number_hits = 0
        self.number_sunk = 0
        self.shots_fired = 0

    @staticmethod
    def get_user_shot():
        mores = False
        more_ = False
        y_axis = None
        x_axis = None
        ls = player_board.board_numbers

        while not mores:  # get x coordinate
            x_axis = raw_input("Choose a X coordinate to fire on (1 - " + str(ls[-1]) + "): ")
            mores = util.try_computer_ship_coordinate(x_axis, ls)

        while not more_:  # get y coordinate
            y_axis = raw_input("Choose a Y coordinate to fire on (1 - " + str(ls[-1]) + "): ")
            more_ = util.try_computer_ship_coordinate(y_axis, ls)

        print "\nFiring",
        util.loading()

        return int(x_axis), int(y_axis)

    @staticmethod
    def beginner():
        ls = player_board.board_numbers

        print "The Computer is firing",
        util.loading()
        x_axis = random.randint(1, int(ls[-1]))
        y_axis = random.randint(1, int(ls[-1]))

        return x_axis, y_axis

    def intermediate(self):
        self.beginner()

    def advanced(self):
        self.beginner()


class Ship:
    def __init__(self, length, ship_name, direction, x, y):
        self.length = length
        self.direction = direction
        self.ship_name = ship_name
        self.x = x
        self.y = y
        self.sunk = False


class Main:
    def __init__(self):
        self.have_won = False
        self.computer_function = {
            "Lieutenant": computer.beginner,
            "Captain": computer.intermediate,
            "Admiral": computer.advanced
        }

    def shoot_to_kill(self):
        while not self.have_won:
            x, y = player.get_user_shot()
            player_board.fire(x, y, "User")

            comp_x, comp_y = self.computer_function[computer.game_mode]()  # let the computer "guess" a coordinate based on skill level
            computer_board.fire(comp_x, comp_y, "cpu")

# *--------| Main |--------* #
# object creation:
screen = Screen()
player_board, player, computer_board, computer, player_fleet, comp_fleet = get_baseline()  # start program and get basic information
main_game = Main()  # create the main object

# main program:
screen.intro_board()
player_fleet.make_ships()
comp_fleet.make_comp_ships()
screen.print_board(computer_board)  # just for testing purposes
screen.battle_intro()  # just a print statement... lol
main_game.shoot_to_kill()
