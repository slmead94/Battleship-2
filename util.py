"""
//**********************************************//

    Battleship 2 utility module
    Assignment: Final Project
    Semester 2, Freshman Year HS
    Started: April 21st, 2016

//**********************************************//
"""
import time


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
            print "Your ship exceeds the ocean boundary! Try again:"
            return True
    except ValueError:
        print "Bad input! Try again:"
        return True


def try_computer_ship_coordinate(num, ls):
    if num in ls:
        return True  # the coordinate is in the used coordinates list return True
    else:
        return False


def loading():
    print ".",
    time.sleep(0.33)
    print ".",
    time.sleep(0.33)
    print ".",
    time.sleep(0.33)
    print


def print_numbered_list(ls):
    # this makes printing a list with numbers in front of each item much more accessible
    for i in range(0, len(ls)):
        print str(i + 1) + ".  " + ls[i]
    print
