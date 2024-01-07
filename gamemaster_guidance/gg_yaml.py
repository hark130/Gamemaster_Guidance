"""Defines package's YML functions."""

# Standard Imports
import sys
import yaml
# Third Party Imports
# Local Imports


def parse_yaml(filename: str) -> dict:
    """Read filename and use yaml to parse it into a dictionary."""
    yaml_dict = None  # Dictionary to return

    try:
        with open(filename, 'r', encoding=sys.getdefaultencoding()) as in_file:
            yaml_dict = yaml.load(in_file, Loader=yaml.FullLoader)
    except Exception as err:
        print(format(err))
        raise err

    return yaml_dict
