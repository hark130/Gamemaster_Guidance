import random


def pick_tuple(filename):
    """Returns a single entry from a newline-delimited file"""
    with open(filename, "r") as inFile:
        fileContent = inFile.read()

    return random.choice(fileContent.split("\n"))
