from GG_Arguments import parse_arguments
from GG_Menu import menu


import sys


def main(argList):
    parse_arguments(argList)
    menu()


if __name__ == "__main__":
    main(sys.argv)
