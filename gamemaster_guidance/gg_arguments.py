"""Implements the packages argument parser."""

# Standard
import getopt
import sys
# Third Party
# Local


def print_help(script_name):
    """Print the usage message."""
    print("\n" + script_name + " -c <cityfile>\n")


def parse_arguments(arg_list):
    """Returns script arguments in a dictionary."""
    # LOCAL VARIABLES
    ret_dict = {}

    try:
        opts, _ = getopt.getopt(arg_list[1:], "hc:", ["cityfile="])
    except getopt.GetoptError:
        print_help(arg_list[0])
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == "-h":
                print_help(arg_list[0])
                sys.exit()
            elif opt in ("-c", "--cityfile"):
                ret_dict["cityfile"] = arg

    return ret_dict
