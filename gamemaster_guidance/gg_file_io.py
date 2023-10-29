"""Implements simplified database wrapper functions."""

# Standard
import random
import sys
# Third Party
# Local


def pick_entry(filename):
    """Returns a single entry from a newline-delimited file"""
    return pick_entries(filename, 1)[0]


def pick_entries(filename, num_tuples, skip_comments=True):
    """Returns a list of strings from a newline-delimited file, skipping comments"""
    # LOCAL VARIABLES
    entry_list = []

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

    # Choose List Entries
    for _ in range(1, num_tuples + 1):
        entry_list.append(random.choice(file_list))

    # DONE
    return entry_list
