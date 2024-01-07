"""Implements simplified database wrapper functions."""

# Standard
from typing import List
import random
import sys
# Third Party
# Local


def pick_entry(filename):
    """Returns a single entry from a newline-delimited file"""
    return pick_entries(filename, 1)[0]


def pick_entries(filename, num_tuples, skip_comments=True):
    """Returns a num_tuples number of strings, in a list, from a newline-delimited file."""
    # LOCAL VARIABLES
    file_list = []   # Full contents of filename.
    entry_list = []  # A subset of the filename entries, of length num_tuples.

    # BUILD LIST
    # Read File
    file_list = read_entries(filename=filename, skip_comments=skip_comments)
    # Choose List Entries
    for _ in range(1, num_tuples + 1):
        entry_list.append(random.choice(file_list))

    # DONE
    return entry_list


def read_entries(filename, skip_comments: bool = True) -> List[str]:
    """Read all entries, as a list of strings, from a newline-delimited file.

    Args:
        filename: A newline-delimited file to read entries from.
        skip_comments: [Optional] Skip any comments in filename.

    Returns: A list of strings read from filename.
    """
    # LOCAL VARIABLES
    file_list = []  # List of strings read from filename.

    # BUILD LIST
    # Open File
    with open(filename, 'r', encoding=sys.getdefaultencoding()) as in_file:
        # Read raw content
        file_content = in_file.read()

    # Split Content
    if skip_comments:
        # Skipping Comments
        file_list = [entry for entry in file_content.split("\n")
                     if not entry.startswith("#") and entry]
    else:
        file_list = [entry for entry in file_content.split("\n") if entry]

    # DONE
    return file_list
