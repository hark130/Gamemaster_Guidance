"""Defines the entry level function for this package."""

# Standard
import locale
# Third Party
# Local
from gamemaster_guidance.gg_arguments import ARG_DICT_KEY_CITY, ARG_DICT_KEY_GANG, parse_arguments
from gamemaster_guidance.gg_menu import menu
from gamemaster_guidance.gg_yaml import parse_yaml


def main():
    """Entry level function for this package."""
    # LOCAL VARIABLES
    city_dict = None   # Dictionary parsed from --cityfile yml
    guild_dict = None  # Dictionary parsed from --guildfile yml

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    parsed_args = parse_arguments()
    if ARG_DICT_KEY_CITY in parsed_args:
        city_dict = parse_yaml(parsed_args[ARG_DICT_KEY_CITY])
    if ARG_DICT_KEY_GANG in parsed_args:
        guild_dict = parse_yaml(parsed_args[ARG_DICT_KEY_GANG])
    menu(city_dict, guild_dict)


if __name__ == "__main__":
    main()
