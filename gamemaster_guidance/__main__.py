from modules.GG_Arguments import parse_arguments
from modules.GG_Menu import menu
from modules.GG_Yaml import parse_yaml


import locale
import sys


def main(argList):
    # LOCAL VARIABLES
    cityDict = None

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    parsedArgs = parse_arguments(argList)
    if "cityfile" in parsedArgs.keys():
        cityDict = parse_yaml(parsedArgs["cityfile"])
    menu(cityDict)


if __name__ == "__main__":
    main(sys.argv)
