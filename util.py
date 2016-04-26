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
