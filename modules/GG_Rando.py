import random


def rand_percent():
    """Return an integer between 1 and 100"""
    return int(100 * random.uniform(0.01, 1.0))