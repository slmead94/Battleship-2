"""
//**********************************************//

Battleship 2 utility module

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
