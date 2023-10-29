"""Implement some randomization functions for the package."""

import random


def rand_percent():
    """Return an integer between 1 and 100"""
    return int(100 * random.uniform(0.01, 1.0))


def rand_integer(min_val, max_val):
    """Return an integer min <= n <= max"""
    # LOCAL VARIABLES
    ret_int = None
    local_min = min_val
    local_max = max_val

    # INPUT VALIDATION
    if not isinstance(min_val, int):
        raise TypeError("min_val is not an integer")
    if not isinstance(max_val, int):
        raise TypeError("max_val is not an integer")
    # Wrong order
    if min_val > max_val:
        local_min = max_val
        local_max = min_val

    # RANDO
    try:
        ret_int = random.randint(local_min, local_max)
    except Exception as err:
        print(repr(err))
        raise err

    # DONE
    return ret_int


def rand_float(start, stop):
    """Return a random float between start and stop"""
    return random.uniform(start, stop)
