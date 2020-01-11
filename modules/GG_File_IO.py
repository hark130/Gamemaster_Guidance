import random


def pick_entry(filename):
    """Returns a single entry from a newline-delimited file"""
    return pick_entries(filename, 1)[0]


def pick_entries(filename, numTuples, skipComments=True):
    """Returns a list of strings from a newline-delimited file, skipping comments"""
    # LOCAL VARIABLES
    listOfEntries = []

    # BUILD LIST
    # Open File
    with open(filename, "r") as inFile:
        # Read raw content
        fileContent = inFile.read()

    # Split Content
    if skipComments:
        # Skipping Comments
        fileList = [entry for entry in fileContent.split("\n") if not entry.startswith("#")]
    else:
        fileList = fileContent.split("\n")

    # Choose List Entries
    for _ in range(1, numTuples + 1):
        listOfEntries.append(random.choice(fileList))

    # DONE
    return listOfEntries
