"""Implements the package's argument parser."""

# Standard
from pathlib import Path
from typing import Dict, Final
import argparse
# Third Party
# Local


# ARGUMENT DICTIONARY KEYS
ARG_DICT_KEY_CITY: Final[str] = 'cityfile'  # -c, --cityfile
ARG_DICT_KEY_GANG: Final[str] = 'gangfile'  # -g, --gangfile


def parse_arguments() -> Dict[str, Path]:
    """Parses the arguments and returns the values in a dictionary."""
    parser = argparse.ArgumentParser(prog='GAMEMASTER GUIDE (GAGU)',
                                     description='Gamemaster aid for Pathfinder 2nd Edition')
    parser.add_argument('-c', '--cityfile', action='store', required=False,
                        help='Filename of a city configuration file')
    parser.add_argument('-g', '--gangfile', action='store', required=False,
                        help='Filename of a gang configuration file')
    parsed_args = parser.parse_args()
    ret_dict = {}

    # City file
    if parsed_args.cityfile:
        ret_dict[ARG_DICT_KEY_CITY] = Path(parsed_args.cityfile)
    # Gang file
    if parsed_args.gangfile:
        ret_dict[ARG_DICT_KEY_CITY] = Path(parsed_args.gangfile)

    for value in ret_dict.values():
        _validate_path(value)

    return ret_dict


def _validate_path(filename: Path) -> None:
    """Validate that filename exists as a file."""
    if not filename.exists():
        raise FileNotFoundError(f'Unable to find {filename.absolute()}')
    if not filename.is_file():
        raise OSError(f'{filename.absolute()} is not a file')
