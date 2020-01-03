import random


def pick_entry(filename):
    """Returns a single entry from a newline-delimited file"""
    with open(filename, "r") as inFile:
        fileContent = inFile.read()

    return random.choice(fileContent.split("\n"))


def pick_entries(filename, numTuples):
    """Returns a list of strings from a newline-delimited file"""
    # LOCAL VARIABLES
    listOfEntries = []

    # BUILD LIST
    # Open File
    with open(filename, "r") as inFile:
        # Read raw content
        fileContent = inFile.read()

    # Split Content
    fileList = fileContent.split("\n")

    # Choose List Entries
    for _ in range(1, numTuples + 1):
        listOfEntries.append(random.choice(fileList))

    # DONE
    return listOfEntries
