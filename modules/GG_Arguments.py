import getopt
import sys


def print_help():
    print("-c <cityfile>")


def parse_arguments(argList):
    """Returns script arguments in a dictionary"""
    # LOCAL VARIABLES
    retDict = {}

    try:
        opts, args = getopt.getopt(argList, "hc:", ["cityfile="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-h":
                print_help()
                sys.exit()
            elif opt in ("-c", "--cityfile"):
                retDict["cityfile"] = arg
        # if "cityfile" in retDict.keys():
        #     print("City file is: %s" % retDict["cityfile"])  # DEBUGGING

    return retDict
