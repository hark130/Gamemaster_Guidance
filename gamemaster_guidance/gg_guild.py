"""Defines the GGGuild class."""

# Standard Imports
# Third Party Imports
# Local Imports
from gamemaster_guidance.gg_globals import FUNC_SPECIAL_LIST
from gamemaster_guidance.gg_job import GGJob
from gamemaster_guidance.gg_misc import (print_header, print_numbered_list, print_rjust_list,
                                         validate_num, validate_percent, validate_scale)


class GGGuild():
    """Generate content for a guild based on a parsed configuration."""

    def __init__(self, guild_dict: dict, num_jobs: int = 10, num_events: int = 3) -> None:
        """Class ctor.

        Args:
            guild_dict: Dictionary parsed from the guild configuration file.
            num_jobs: [Optional] Number of jobs to randomize at once.  Valid integers: 1 - 100.
            num_events: [Optional] Number of events to randomize at once.  Valid integers: 1 - 100.
        """
        self._guild_dict = guild_dict  # Input dictionary
        self._num_jobs = num_jobs      # Number of jobs to randomize at once
        self._num_events = num_events  # Number of events to randomize at once
        self._job_obj = None           # GGJob object
        self._validated = False        # Controls internal validation

    ##################
    # PUBLIC METHODS #
    ##################
    # Organized in suggested call order

    def print_guild_config(self) -> None:
        """Print all details about the guild."""
        self._validate_input()
        self._print_guild_config()

    def rando_events(self) -> None:
        """Randomize and print a pre-determined number of guild events."""
        self._validate_input()
        print("TO DO: DON'T DO NOW... Implement rando_events()")

    def rando_jobs(self) -> None:
        """Randomize and print a pre-determined number of jobs based on guild specialities."""
        # LOCAL VARIABLES
        job_list = []  # List of randomized jobs

        # VALIDATE INPUT
        self._validate_input()
        if not self._job_obj:
            self._job_obj = GGJob(special_dict=self._guild_dict['guild']['specialties'],
                                  goals=self._guild_dict['guild']['design']['goals'],
                                  territory=self._guild_dict['guild']['design']['territory'])

        # PRINT IT
        job_list = self._job_obj.rando_jobs(num_jobs=self._num_jobs)
        print_numbered_list(print_list=job_list, header='Job List')

    def get_num_events(self) -> int:
        """Get the current number of events to randomize at once."""
        self._validate_input()
        return self._num_events

    def get_num_jobs(self) -> int:
        """Get the current number of jobs to randomize at once."""
        self._validate_input()
        return self._num_jobs

    ###################
    # PRIVATE METHODS #
    ###################
    # Organized alphabetically

    def _print_guild_alignment(self) -> None:
        """Print the guild alignment."""
        # LOCAL VARIABLES
        print_list = []  # List of strings to print, right-justified

        # PRINT IT
        print_header('ALIGNMENT')
        print_list.append(f"Morals {self._guild_dict['guild']['alignment']['morals']}")
        print_list.append(f"Ethics {self._guild_dict['guild']['alignment']['ethics']}")
        print_rjust_list(print_list)
        print('')

    def _print_guild_config(self) -> None:
        """Print all details about the guild."""
        # Name
        print_header(self._guild_dict['guild']['details']['name'].upper())

        # Region
        print(f"Location: {self._guild_dict['guild']['details']['location']}\n")

        # Alignment
        self._print_guild_alignment()

        # Design
        self._print_guild_design()

        # Specialties
        self._print_guild_specialties()

        # DONE
        print('')

    def _print_guild_design(self) -> None:
        """Print the guild design."""
        # LOCAL VARIABLES
        print_list = []  # List of strings to print, right-justified

        # PRINT IT
        print_header('DESIGN')
        print_list.append(f"Goals {self._guild_dict['guild']['design']['goals']}")
        print_list.append(f"Territory {self._guild_dict['guild']['design']['territory']}")
        print_rjust_list(print_list)
        print('')

    def _print_guild_specialties(self) -> None:
        """Print the guild specialties."""
        # LOCAL VARIABLES
        # List of functional specialty keys
        func_specials = FUNC_SPECIAL_LIST
        temp_val = 0     # Temp value variable while iterating the dictionary
        print_list = []  # List of strings to print at a fixed width

        # PRINT IT
        print_header('SPECIALTIES')
        for func_special in func_specials:
            temp_val = self._guild_dict['guild']['specialties'][func_special]
            if temp_val:
                print_list.append(f'{func_special.capitalize()}: {temp_val: >3}%')
        print_rjust_list(print_list)

        # DONE
        print('')

    def _validate_guild(self) -> None:
        """Validates self._guild_dict."""
        # LOCAL VARIABLES
        top_key = 'guild'                                                  # Top key
        key_detail = 'details'                                             # Mandatory key
        key_align = 'alignment'                                            # Mandatory key
        key_design = 'design'                                              # Mandatory key
        key_special = 'specialties'                                        # Mandatory key
        mandatory_keys = [key_detail, key_align, key_design, key_special]  # Mandatory sub-keys

        # VALIDATE IT
        if self._guild_dict:
            if isinstance(self._guild_dict, dict):
                for mandatory_key in mandatory_keys:
                    if mandatory_key not in self._guild_dict[top_key].keys():
                        raise KeyError(f'Unable to find mandatory key "{mandatory_key}" in '
                                       'guild_dict input')
                self._validate_guild_details(self._guild_dict[top_key][key_detail])
                self._validate_guild_alignment(self._guild_dict[top_key][key_align])
                self._validate_guild_design(self._guild_dict[top_key][key_design])
                self._validate_guild_specialties(self._guild_dict[top_key][key_special])
            else:
                raise TypeError('The guild_dict argument was not a dictionary.')
        else:
            raise ValueError('The guild_dict argument is mandatory')

        # DONE
        self._validated = True  # If we made it here, everything checks out

    def _validate_guild_alignment(self, alignment: dict) -> None:
        """Validate the guild alignment."""
        # LOCAL VARIABLES
        dict_key = 'alignment'                 # Name of the guild key being validated
        mandatory_keys = ['morals', 'ethics']  # Mandatory sub-keys

        # VALIDATE ALIGNMENT
        for found_key in alignment.keys():
            if found_key in mandatory_keys:
                validate_scale(alignment[found_key], f"{dict_key}'s {found_key}")
            else:
                raise RuntimeError(f'Discovered errant guild {dict_key} entry: {found_key}')

    def _validate_guild_design(self, design: dict) -> None:
        """Validate the guild design."""
        # LOCAL VARIABLES
        dict_key = 'alignment'                   # Name of the guild key being validated
        mandatory_keys = ['goals', 'territory']  # Mandatory sub-keys

        # VALIDATE DESIGN
        for found_key in design.keys():
            if found_key in mandatory_keys:
                validate_scale(design[found_key], f"{dict_key}'s {found_key}")
            else:
                raise RuntimeError(f'Discovered errant guild {dict_key} entry: {found_key}')

    def _validate_guild_details(self, details: dict) -> None:
        """Validate the guild details."""
        # LOCAL VARIABLES
        dict_key = 'details'                   # Name of the guild key being validated
        mandatory_keys = ['name', 'location']  # Mandatory sub-keys

        # VALIDATE DETAILS
        for found_key in details.keys():
            if found_key in mandatory_keys:
                if not isinstance(details[found_key], str):
                    raise TypeError(f'The {dict_key} {found_key} must be of type string"')
                if not details[found_key]:
                    raise ValueError(f'The {dict_key} {found_key} may not be empty')
            else:
                raise RuntimeError(f'Discovered errant guild {dict_key} entry: {found_key}')

    def _validate_guild_specialties(self, specialties: dict) -> None:
        """Validate the guild specialties."""
        # LOCAL VARIABLES
        dict_key = 'specialties'  # Name of the guild key being validated
        # Mandatory sub-keys
        mandatory_keys = FUNC_SPECIAL_LIST

        # VALIDATE ALIGNMENT
        for found_key in specialties.keys():
            if found_key in mandatory_keys:
                validate_percent(specialties[found_key], f"{dict_key}'s {found_key}",
                                 can_be_zero=True)
            else:
                raise RuntimeError(f'Discovered errant guild {dict_key} entry: {found_key}')

    def _validate_input(self) -> None:
        """Validate ctor input.

        Call this method in every public method.
        """
        # INPUT VALIDATION
        if self._validated is False:
            # guild_dict
            self._validate_guild()
            # num_jobs
            validate_num(value=self._num_jobs, name='num_jobs')
            # num_events
            validate_num(value=self._num_events, name='num_events')

            # DONE
            self._validated = True
