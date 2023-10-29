"""Defines the entry level function for this package."""

# Standard
import locale
import sys
# Third Party
# Local
from gamemaster_guidance.gg_arguments import parse_arguments
from gamemaster_guidance.gg_menu import menu
from gamemaster_guidance.gg_yaml import parse_yaml


def main():
    """Entry level function for this package."""
    # LOCAL VARIABLES
    city_dict = None

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    parsed_args = parse_arguments()
    if 'cityfile' in parsed_args:
        city_dict = parse_yaml(parsed_args['cityfile'])
    menu(city_dict)


if __name__ == "__main__":
    main()
