"""
//------------------------------------------------------------------//
                        *--Battleship 2--*
//******************************************************************//

    Spencer M.
    Assignment: Final Project
    Semester 2, Freshman Year HS
    Started: April 20th, 11:30, 2016

//******************************************************************//

    The user needs to be careful when placing ships because there is no
    overlapping algorithm so you can cheat and only have a few ships on
    the board...

    Also, the advanced skill level that the computer has isn't the best
    but it works... I wanted to get the code that I already had working
    well before I did anything heroic.

//******************************************************************//

    Git repository:   https://github.com/slmead94/Battleship-2

//******************************************************************//
"""
import util
import random


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

    def add_ship(self, ship, board):
        """
        :param ship: The ship object that contains all of the data needed to put the ship on the given board
        :param board: the given board that the ship is going to be placed on to
        """

        global player_board, computer_board
        is_i = None  # the variable that will take on the value of i in the for loop, but could be made negative
        symbol = None  # the symbol needed for the ship to be "looking" the right direction

        # we have to decrement the coordinates so they conform to the ways of the list
        ship.y = int(ship.y) - 1
        ship.x = int(ship.x) - 1

        if ship.direction == "U" or ship.direction == "D":
            for i in range(0, ship.length):

                if ship.direction == "U":
                    symbol = self.ship_up
                    is_i = i
                elif ship.direction == "D":
                    symbol = self.ship_down
                    is_i = i / -1

                board.main_board[ship.y + is_i][ship.x] = symbol
                appendix = [ship.y + is_i, ship.x]
                ship.coords.append(appendix)

        elif ship.direction == "L" or ship.direction == "R":
            for i in range(0, ship.length):

                if ship.direction == "L":
                    symbol = self.ship_left
                    is_i = i
                elif ship.direction == "R":
                    symbol = self.ship_right
                    is_i = i / -1

                board.main_board[ship.y][ship.x + is_i] = symbol
                appendix = [ship.y, ship.x + is_i]
                ship.coords.append(appendix)

        if board.header == "Player Board":
            print
            player_board = board
            screen.print_board(player_board)
        else:
            computer_board = board


class Game:
    def __init__(self):
        self.hit = "X"
        self.miss = "*"
        self.empty = "_"
        self.ship_types = ["V", "<", ">", "^"]
        self.used = []
        self.last = []
        self.last_was_hit = False
        self.computer_x = None
        self.computer_y = None

    def fire(self, x, y, who):
        x_axis = int(x) - 1  # decrement the variables so they can work correctly with lists
        y_axis = int(y) - 1

        if who.upper() == "USER":
            if computer_board.main_board[y_axis][x_axis] in self.ship_types:
                print "You have hit a ship!\n"
                computer_board.main_board[y_axis][x_axis] = self.hit
                player_spectate.main_board[y_axis][x_axis] = self.hit
                player.number_hits += 1

                hit_ship = player_fleet.find_hit_ship(x, y)
                self.sunk_tester(hit_ship, computer_board)

            elif computer_board.main_board[y_axis][x_axis] == self.empty:
                print "Miss\n"
                computer_board.main_board[y_axis][x_axis] = self.miss
                player_spectate.main_board[y_axis][x_axis] = self.miss
                player.number_missed += 1

            screen.print_board(player_spectate)
            player.shots_fired += 1
            raw_input("Press return to continue: ")
        else:
            if player_board.main_board[y_axis][x_axis] in self.ship_types:
                print "You have been hit!!!\n"
                player_board.main_board[y_axis][x_axis] = self.hit
                computer.number_hits += 1
                game.last_was_hit = True

                c_hit_ship = comp_fleet.find_hit_ship(x, y)
                self.sunk_tester(c_hit_ship, player_board)

            elif player_board.main_board[y_axis][x_axis] == self.empty:
                print "The computer missed you\n"
                player_board.main_board[y_axis][x_axis] = self.miss
                computer.number_missed += 1
                game.last_was_hit = False

            computer.shots_fired += 1
            screen.print_board(player_board)

    def sunk_tester(self, ship, board):
        counted = 0

        for i in range(0, len(ship.coords)):
            if board.main_board[ship.coords[i][0]][ship.coords[i][1]] == self.hit:
                counted += 1

        if counted == ship.length:
            ship.sunk = True
            if ship.ship_name[0:1] == "C":
                print "You have sunk the " + ship.ship_name + "!"
                player.number_sunk += 1
            else:
                print "Your " + ship.ship_name + ' has been sunk by the computer!\n'
                computer.number_sunk += 1

    def get_user_shot(self):
        more = True
        y_axis = None
        x_axis = None
        ls = player_board.board_numbers

        while more:
            current_try = []  # array that will hold the user's new guess
            mores = False
            more_ = False

            while not mores:  # get x coordinate
                x_axis = raw_input("Choose an X coordinate to fire on (1 - " + str(ls[-1]) + "): ")
                mores = util.try_computer_ship_coordinate(x_axis, ls)

            while not more_:  # get y coordinate
                y_axis = raw_input("Choose a Y coordinate to fire on (1 - " + str(ls[-1]) + "): ")
                more_ = util.try_computer_ship_coordinate(y_axis, ls)

            current_try.append(x_axis)  # append the coordinates to the list to compare with the used list
            current_try.append(y_axis)

            if current_try in self.used:
                print "You've already fired on the coordinate... Try again:\n"
                more = True
            else:
                self.used.append(current_try)
                more = False

        print "\nFiring",
        util.loading()

        return int(x_axis), int(y_axis)

    @staticmethod
    def beginner():  # there is literally no way the user couldn't win
        ls = player_board.board_numbers

        print "\nThe Computer is firing",
        util.loading()
        x_axis = random.randint(1, int(ls[-1]))
        y_axis = random.randint(1, int(ls[-1]))
        print "(" + str(x_axis) + ", " + str(y_axis) + ")"

        return x_axis, y_axis

    def advanced(self):  # this method is a little sloppy if you know what I mean, but it works...roughly
        pre_done = False

        if computer.shots_fired == 0:  # if this is the computer's first move, put it the center of the board
            if len(player_board.board_numbers) == 20:
                self.computer_x = 10
                self.computer_y = 10
            elif len(player_board.board_numbers) == 15:
                self.computer_x = 8
                self.computer_y = 8
            elif len(player_board.board_numbers) == 10:
                self.computer_x = 5
                self.computer_y = 5

            self.last = [self.computer_x, self.computer_y]
            return self.computer_x, self.computer_y

        elif self.last_was_hit:
            if self.last[1] != 1:
                self.computer_x = self.last[0]
                self.computer_y = self.last[1] + 1
            elif self.last[0] != len(player_board.board_numbers):
                self.computer_x = self.last[0] + 1
                self.computer_y = self.last[1]

        elif self.last[0] > len(player_board.board_numbers) - 1:
            self.computer_x = self.last[0]
            self.computer_y = self.last[1] - 2
        elif self.last[1] > len(player_board.board_numbers) - 1:
            self.computer_x = self.last[0] - 2
            self.computer_y = self.last[1]
        else:
            self.computer_x += 1
            self.computer_y += 1

        if not pre_done:
            self.last = [self.computer_x, self.computer_y]
            return self.computer_x, self.computer_y


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
        print "|-|*****************************************************|-|"
        print "\nYou will fire at the opponent by choosing an X and Y coordinate."

    @staticmethod
    def congrats_winner(winner):
        if winner.upper() == "USER":
            print "Congratulations!!"
            print "You have beaten the computer!"
        else:
            print "Well... You lost..."
            print "Better luck next time!"

        print "\n\tFinal Player Stats:\n"
        print "Total Shots fired: " + str(player.shots_fired)
        print "Total hits: " + str(player.number_hits)
        print "Total ships sunk: " + str(player.number_sunk)
        print "Total misses: " + str(player.number_missed)
        print

    def print_board(self, board_object):
        i = 0

        print board_object.header
        print "    ",
        for i in range(0, len(board_object.board_numbers)):  # print the numbers
            if i < 9:  # if the board is double digits take away one space to keep it even
                print board_object.board_numbers[i] + "  ",
            else:
                print board_object.board_numbers[i] + " ",
        self.other_line = "    " + "____" * (i + 1)
        self.other_line = self.other_line[:-1]
        print  # space

        print self.other_line
        for rows in range(0, board_object.height):
            if rows < 9:  # if the board is a double digit board, like: 15x15 or 20x20, take away 1 space
                print str(rows + 1) + " ",
            else:
                print str(rows + 1),
            for columns in range(0, board_object.width):
                print self.spacer + board_object.main_board[rows][columns],
            print self.spacer
        print


class Ship:
    def __init__(self, length, ship_name, direction, x, y):
        self.length = length
        self.direction = direction
        self.ship_name = ship_name
        self.x = x
        self.y = y
        self.coords = []
        self.sunk = False


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

    def find_hit_ship(self, x, y):
        if self.who.upper() == "USER":
            for i in range(0, len(comp_fleet.ships)):
                if x - 1 == comp_fleet.ships[i].x:
                    return comp_fleet.ships[i]

        elif self.who.upper() == "COMPUTER":
            x_axis = x - 1
            y_axis = y - 1

            for j in range(0, len(player_fleet.ships)):
                if [y_axis, x_axis] in player_fleet.ships[j].coords:
                    return player_fleet.ships[j]

    def make_computer_ships(self):
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
            comp_fleet.ships.append(new_ship)
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
            util.print_numbered_list(self.directions)

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
            player_fleet.ships.append(new_ship)  # append the newest ship to the ships list
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


def get_baseline():
    chosen_level = None
    chosen_type = None
    more = True
    continue_ = True
    battlefield_types = [[10, 10], [15, 15], [20, 20]]  # 10 X 10, 15 X 15, 20 X 20
    game_modes = ["Lieutenant", "Captain"]  # different Naval Ranks for the skill levels

    print "\tWelcome to Battleship 2!\n"
    name = raw_input("Enter your name: ")  # name please?

    print "\nYou may choose from " + str(len(battlefield_types)) + " different battlefield types: (less space - easier to hit each other)\n"
    for i in range(0, len(battlefield_types)):
        print str(i + 1) + ".   " + str(battlefield_types[i][0]) + " X " + str(battlefield_types[i][1])  # print list in format

    while more:  # verification loop
        chosen_type = raw_input("Choose one of the above numbers: ")
        more = util.try_int(chosen_type, [1, 2, 3])

    print "\nYou may choose from " + str(len(game_modes)) + " different game modes to play:\n"
    util.print_numbered_list(game_modes)

    while continue_:
        chosen_level = raw_input("Choose one of the above numbers: ")
        continue_ = util.try_int(chosen_level, [1, 2])

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
    new_spectate_board = Battlefield(height, width, "Player Spectate Board")
    new_spectate_board.fill_board()

    return new_board, new_player, comp_board, comp_player, p_fleet, c_fleet, new_spectate_board  # return the new objects to be used in Main


class Main:
    def __init__(self):
        self.have_won = False
        self.computer_function = {
            "Lieutenant": game.beginner,
            "Captain": game.advanced,
        }

    def shoot_to_kill(self):  # this is the real "main"
        screen.battle_intro()  # just a print statement... lol
        while not self.have_won:  # while no one has won
            x, y = game.get_user_shot()
            game.fire(x, y, "User")
            self.check_status()

            comp_x, comp_y = self.computer_function[computer.game_mode]()  # let the computer "guess" a coordinate based on skill level
            game.fire(comp_x, comp_y, "cpu")
            self.check_status()  # see if someone has won the game yet

        if player.winner:
            won = "user"
        else:
            won = "cpu"
        screen.congrats_winner(won)

    def check_status(self):
        if player.number_hits == comp_fleet.total_lengths or player.number_sunk == len(comp_fleet.ships):
            self.have_won = True
            player.winner = True

        elif computer.number_hits == player_fleet.total_lengths or computer.number_sunk == len(player_fleet.ships):
            self.have_won = True
            computer.winner = True

# *--------| Main |--------* #
# object creation:
screen = Screen()
game = Game()
player_board, player, computer_board, computer, player_fleet, comp_fleet, player_spectate = get_baseline()  # start program and get game information
main_game = Main()  # create the main object

# main program:
screen.intro_board()
player_fleet.make_ships()
comp_fleet.make_computer_ships()
# screen.print_board(computer_board)  # for testing purposes only ; un-commenting this line allows you to see the opponents board
main_game.shoot_to_kill()  # init main game
