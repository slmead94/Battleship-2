"""
//**********************************************//

    Battleship 2 utility module
    Assignment: Final Project
    Semester 2, Freshman Year HS
    Started: April 21st, 2016

//**********************************************//
"""


def try_int(num, ls):
    try:
        int(num)
        if int(num) in ls:
            return False
        else:
            print "Bad input! Try again:"
            return True
    except ValueError:
        print "Bad input! Try again:"
        return True


def try_battlefield_int(num, ls):
    try:
        int(num)
        if num in ls:
            return False
        else:
            print "Bad input! Try again:"
            return True
    except ValueError:
        print "Bad input! Try again:"
        return True


def try_computer_ship_coordinate(num, ls):
    if num in ls:
        return True  # the coordinate is in the used coordinates list return True
    else:
        return False
