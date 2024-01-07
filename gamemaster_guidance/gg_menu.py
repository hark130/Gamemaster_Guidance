"""Implements command-line menu functionality for the package."""

# Standard
from collections import OrderedDict
from typing import Final, List
import subprocess
# Third Party
import platform
# Local
from gamemaster_guidance.gg_ancestry import GGAncestry
from gamemaster_guidance.gg_bounty import GGBounty
from gamemaster_guidance.gg_character import GGCharacter
from gamemaster_guidance.gg_city import GG_City
from gamemaster_guidance.gg_globals import ANCESTRY_LIST
from gamemaster_guidance.gg_guild import GGGuild


# Formation of the race-based menu dictionary
_RACE_DICT_BEGIN: Final[List] = [(1, None)]  # Beginning of the menu list
_RACE_DICT_END: Final[List] = []  # End of the menu list (see: GAGU-19)
# Starting value for additional menu items
try:
    _MENU_CHOICE_START: Final[int] = _RACE_DICT_BEGIN[-1][0] + 1
except IndexError:
    _MENU_CHOICE_START: Final[int] = 1
# Lookup of race menu selection to actual race
RACE_DICT: Final[dict] = \
    OrderedDict(_RACE_DICT_BEGIN + [(count + _MENU_CHOICE_START, value) for (count, value)
                                    in enumerate(ANCESTRY_LIST)] + _RACE_DICT_END)


def city_menu(city_obj):
    """Print the city menu and read user input."""
    clear_screen()
    user_input = None  # Stores user input

    while user_input != 999:
        print_city_menu()
        user_input = read_user_input()
        if user_input == 1:
            if city_obj:
                clear_screen()
                city_obj.print_city_details()
            else:
                print('\nNo city config provided')
                return 999
        elif user_input == 2:
            if city_obj:
                clear_screen()
                city_obj.print_city_npcs()
            else:
                print('\nNo city config provided')
                return 999
        elif user_input == 3:
            clear_screen()
        elif user_input == 42:
            return user_input
        else:
            return 999


def clear_screen():
    """Clear the screen in an operating system friendly way."""
    os_name = platform.system()
    if os_name in ('Linux', 'Darwin'):
        command = 'clear'
    elif os_name == 'Windows':
        command = 'cls'
    else:
        for _ in range(0, 60):
            print('\n')
        return

    subprocess.call([command], shell=True)


def guild_menu(guild_obj):
    """Print the guild menu and read user input."""
    clear_screen()
    user_input = 0  # Stores user input
    num_jobs = 0    # Number of jobs to randomize
    num_events = 0  # Number of events to randomize

    # INPUT VALIDATION
    if not guild_obj:
        print('\nNo guild config provided')
        user_input = 999

    # GUILD MENU
    while user_input != 999:
        num_jobs = guild_obj.get_num_jobs()
        num_events = guild_obj.get_num_events()
        print_guild_menu(num_jobs=num_jobs, num_events=num_events)
        user_input = read_user_input()
        # Guild details
        if user_input == 1:
            clear_screen()
            guild_obj.print_guild_config()
        # Randomize jobs
        elif user_input == 2:
            clear_screen()
            guild_obj.rando_jobs()
        # Randomize event
        elif user_input == 3:
            clear_screen()
            guild_obj.rando_events()
        # Clear screen
        elif user_input == 4:
            clear_screen()
        # Main menu
        elif user_input == 42:
            break
        # Exit
        else:
            user_input = 999

    # DONE
    return user_input


def menu(city_dict: dict, guild_dict: dict) -> None:
    """Top level menu.

    Args:
        city_dict: Dictionary parsed from the city configuration file.  Can be None.
        guild_dict: Dictionary parsed from the guild configuration file.  Can be None.
    """
    # LOCAL VARIABLES
    user_input = 0    # User integer input
    city_obj = None   # GGCity() object
    guild_obj = None  # GGGuild() object

    # SETUP
    clear_screen()
    print('\nWelcome to Gamemaster Guidance')
    if city_dict:
        city_obj = GG_City(city_dict)
        city_obj.load()
    if guild_dict:
        guild_obj = GGGuild(guild_dict)

    # START
    while user_input != 999:
        print('\n')
        print('  1. Randomize a name')
        print('  2. Randomize a character')
        print('  3. Randomize a bounty')
        print('  4. City menu')
        print('  5. Guild menu')
        print('  6. Clear screen')
        print('999. Exit')
        print('Choose an option [999]:')
        user_input = read_user_input()
        if user_input == 1:
            user_input = rando_a_name()
        elif user_input == 2:
            user_input = rando_a_character(city_obj)
        elif user_input == 3:
            user_input = rando_a_bounty(city_obj)
        elif user_input == 4:
            user_input = city_menu(city_obj)
        elif user_input == 5:
            user_input = guild_menu(guild_obj)
        elif user_input == 6:
            clear_screen()
        elif user_input == 999:
            pass
        elif user_input == -1:
            user_input = 999
        else:
            raise SystemExit('Exiting Gamemaster Guidance')

    # DONE
    print('\nThank you for using Gamemaster Guidance\n')


def print_bounty_menu():
    """Print the bounty menu."""
    print('\n')
    print("  1. Choose bounty's minimum level")
    print("  2. Choose bounty's race")
    print('  3. Clear screen')
    print(' 42. Main Menu')
    print('999. Exit')
    print('Choose an option [999]:')


def print_city_menu():
    """Print the city menu."""
    print('\n')
    print('  1. Print the city details')
    print('  2. Print the NPCs')
    print('  3. Clear screen')
    print(' 42. Main Menu')
    print('999. Exit')
    print('Choose an option [999]:')


def print_guild_menu(num_jobs: int, num_events: int) -> None:
    """Print the guild menu."""
    # LOCAL VARIABLES
    job_suffix = 's'    # Default to plural jobs
    event_suffix = 's'  # Default to plural events

    # VARIABLE PRINTING
    if num_jobs == 1:
        job_suffix = ''
    if num_events == 1:
        event_suffix = ''

    # PRINT IT
    print('\n')
    print('  1. Print the guild details')
    print(f'  2. Randomize {num_jobs} job{job_suffix}/score{job_suffix}')
    print(f'  3. Randomize {num_events} event{event_suffix}')
    print('  4. Clear screen')
    print(' 42. Main Menu')
    print('999. Exit')
    print('Choose an option [999]:')


def print_race_menu():
    """Print a selection menu of races."""
    print('\n')
    for key, value in RACE_DICT.items():
        if not value:
            value = 'Random race'
        print(f'  {key}. {value}')
    print(' 42. Main Menu')
    print('999. Exit')
    print('Choose an option [999]:')


def rando_a_bounty_level(city_obj=None):
    """Read user's desired minimum bounty level and return a bounty object."""
    print("\nEnter bounty's minimum level:")
    minimum_level = read_user_input()

    if minimum_level < 1:
        raise RuntimeError('Level too low')
    if minimum_level > 20:
        raise RuntimeError('Level too high')

    try:
        bounty = GGBounty(city_object=city_obj, minLevel=minimum_level)
    except RuntimeError as err:
        print(format(err))
        bounty = None

    return bounty


def rando_a_bounty(city_obj=None):
    """Randomize a bounty menu item based on user input."""
    print_bounty_menu()
    user_input = read_user_input()
    bounty = None

    try:
        if user_input == 1:
            bounty = rando_a_bounty_level(city_obj)
        elif user_input == 2:
            bounty = rando_a_bounty_race(city_obj)
        elif user_input == 3:
            clear_screen()
        elif user_input == 42:
            bounty = None
        else:
            raise SystemExit('Exiting Gamemaster Guidance')
    except RuntimeError as err:
        print(format(err))
    else:
        if bounty:
            clear_screen()
            bounty.print_all_details()

    return user_input


def rando_a_bounty_race(city_obj=None):
    """Randomize and print a bounty race based on ther user's selected race."""
    # LOCAL VARIABLES
    bounty = None  # GGBounty() object
    print_race_menu()
    user_input = read_user_input()

    try:
        if user_input in RACE_DICT.keys():
            if not RACE_DICT[user_input]:
                bounty = GGBounty(city_object=city_obj)
            else:
                bounty = GGBounty(race=RACE_DICT[user_input], city_object=city_obj)
        elif user_input != 42:
            raise SystemExit('Exiting Gamemaster Guidance')
    except RuntimeError as err:
        print(format(err))

    return bounty


def rando_a_character(city_obj=None):
    """Randomize and print a character based on ther user's selected race."""
    print_race_menu()
    user_input = read_user_input()

    try:
        if user_input in RACE_DICT.keys():
            if not RACE_DICT[user_input]:
                character = GGCharacter(city_object=city_obj)
            else:
                character = GGCharacter(race=RACE_DICT[user_input], city_object=city_obj)
        elif user_input != 42:
            raise SystemExit('Exiting Gamemaster Guidance')
    except RuntimeError as err:
        print(format(err))
    else:
        if character:
            character.print_character()

    return user_input


def rando_a_name():
    """Randomize and print a name based on the user's selected race."""
    print_race_menu()
    user_input = read_user_input()

    try:
        if user_input in RACE_DICT.keys():
            if not RACE_DICT[user_input]:
                char_name = GGAncestry()
            else:
                char_name = GGAncestry(race=RACE_DICT[user_input])
        elif user_input != 42:
            raise SystemExit('Exiting Gamemaster Guidance')
    except RuntimeError as err:
        print(format(err))
        raise err
    else:
        if char_name:
            print(f'\n{char_name.return_full_name()}\n')

    return user_input


def read_user_input():
    """Read an integer from user input.  Return -1 on error"""
    user_input = input()
    try:
        user_choice = int(user_input)
    except (TypeError, ValueError):
        user_choice = int(-1)

    return user_choice
