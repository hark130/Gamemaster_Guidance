"""Defines the GGJob class."""

# Standard Imports
from typing import Any, List
# Third Party Imports
# Local Imports
from gamemaster_guidance.gg_globals import FUNC_SPECIAL_LIST


class GGJob():
    """Generate one or more jobs based on functional specialties."""

    def __init__(self, special_dict: dict = None) -> None:
        """Class ctor.

        Args:
            special_dict: [Optional] Expects FUNC_SPECIAL_LIST entries as keys and %s as values.
                Can be None.  If None, the class will assume an equal distribution across the
                functional specialties.
        """
        self._special_dict = special_dict  # Input dictionary
        self._validated = False            # Controls internal validation

    ### PUBLIC METHODS ###
    # Organized in suggested call order

    def rando_job(self) -> str:
        """Randomize one job."""
        # INPUT VALIDATION
        self._validate_input()

        # RANDO IT
        return self._rando_job()

    def rando_jobs(self, num_jobs: int) -> List[str]:
        """Create a list of random jobs."""
        # LOCAL VARIABLES
        job_list = []  # List of random jobs

        # INPUT VALIDATION
        self._validate_input()
        validate_num(num_jobs, 'num_jobs argument')

        # RANDO IT
        for _ in range(num_jobs):
            job_list.append(self.rando_job())

        # DONE
        return job_list

    ### PRIVATE METHODS ###
    # Organized alphabetically



    def _validate_input(self) -> None:
        """Validate ctor input.

        Call this method in every public method.
        """
        # INPUT VALIDATION
        if self._validated is False:
            # special_dict
            self._validate_special_dict()

            # DONE
            self._validated = True

    def _validate_special_dict(self) -> None:
        """Validate the special dict."""
        # Empty?  Populate it.
        if not self._special_dict:
            self._special_dict = {}  # Reset the dict (in case it was some other empty container)
            for func_special_entry in FUNC_SPECIAL_LIST:
                self._special_dict[func_special_entry] = int(100 / len(FUNC_SPECIAL_LIST))
        # Validate contents
        if not isinstance(self._special_dict, dict):
            raise TypeError('The special_dict argument must be of type dict')
        for func_special_entry in FUNC_SPECIAL_LIST:
            if func_special_entry not in self._special_dict.keys():
                raise KeyError(f'Unable to find mandatory key "{func_special_entry}" in '
                               'special_dict input')
            validate_percent(self._special_dict[func_special_entry], func_special_entry)
        for found_key in self._special_dict.keys():
            if found_key not in FUNC_SPECIAL_LIST:
                raise RuntimeError(f'Discovered errant specialty dict entry: {found_key}')
