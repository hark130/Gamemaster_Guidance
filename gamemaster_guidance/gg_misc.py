"""Defines miscellaneous functions for the package."""

# Standard Imports
from typing import Any, List
# Third Party Imports
# Local Imports


def print_header(header: str) -> None:
    """Print a header surrounded by a standardized banner."""
    # LOCAL VARIABLES
    banner = '-' * len(header)

    print(banner)
    print(header)
    print(banner)


def print_numbered_list(print_list: List[str], header: str = None) -> None:
    """Print list contents in a numbered list under an optional header."""
    if header:
        print_header(header=header)
    for num, print_entry in enumerate(print_list):
        temp_num = f'{num + 1}'
        print((' ' * (len(str(len(print_list))) - len(temp_num)))
              + f'{temp_num}. {print_entry}')


def print_rjust_list(str_list: List[str]) -> None:
    """Print a list of strings, right-justified to the width of the longest string."""
    # LOCAL VARIABLES
    longest_str = 0  # Length of the longest string in str_list

    # INPUT VALIDATION
    if not isinstance(str_list, list):
        raise TypeError('The str_list argument must be of type list')
    for str_list_entry in str_list:
        if not isinstance(str_list_entry, str):
            raise TypeError('A non-string was found in str_list')
        if len(str_list_entry) > longest_str:
            longest_str = len(str_list_entry)

    # PRINT IT
    for str_list_entry in str_list:
        print(f"{(longest_str - len(str_list_entry)) * ' '}{str_list_entry}")


def validate_int_scale(value: int, name: str) -> None:
    """Validate value is an integer on an inclusive scale of 1 to 10.

    Args:
        value: Value to test as a number on a scale of 1 to 10.
        name: Argument name being validated.  Used to format exception messages.
    """
    # INPUT VALIDATION
    if not isinstance(value, int):
        raise TypeError(f'The {name} must be of type int')
    validate_scale(value=value, name=name)


def validate_num(value: int, name: str) -> None:
    """Validate value is an integer between 1 and 100, inclusive.

    Args:
        value: Integer to test.
        name: Argument name being validated.  Used to format exception messages.
    """
    # INPUT VALIDATION
    if not isinstance(value, int):
        raise TypeError(f'The {name} must be of type int')
    validate_percent(value=value, name=name)


def validate_percent(value: Any, name: str, can_be_zero: bool = False) -> None:
    """Validate value is an integer or float on an inclusive range of 1 to 100.

    Args:
        value: Value to test as a percentage.
        name: Argument name being validated.  Used to format exception messages.
    """
    # INPUT VALIDATION
    if isinstance(value, (float, int)):
        if value == 0 and can_be_zero:
            pass
        elif value < 1:
            raise ValueError(f'The {name} may not be less than 1')
        if value > 100:
            raise ValueError(f'The {name} may not be more than 100')
    else:
        raise TypeError(f'The {name} must be of type int or float')


def validate_scale(value: Any, name: str) -> None:
    """Validate value is an integer or float on an inclusive scale of 1 to 10.

    Args:
        value: Value to test as a number on a scale of 1 to 10.
        name: Argument name being validated.  Used to format exception messages.
    """
    # INPUT VALIDATION
    if isinstance(value, (float, int)):
        if value < 1:
            raise ValueError(f'The {name} may not be less than 1')
        if value > 10:
            raise ValueError(f'The {name} may not be more than 10')
    else:
        raise TypeError(f'The {name} must be of type int or float')
