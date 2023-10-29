import getopt
import sys


def print_help(scriptName):
    print("\n" + scriptName + " -c <cityfile>\n")


def parse_arguments(argList):
    """Returns script arguments in a dictionary"""
    # LOCAL VARIABLES
    retDict = {}

    try:
        opts, args = getopt.getopt(argList[1:], "hc:", ["cityfile="])
    except getopt.GetoptError:
        print_help(argList[0])
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-h":
                print_help(argList[0])
                sys.exit()
            elif opt in ("-c", "--cityfile"):
                retDict["cityfile"] = arg

    return retDict
