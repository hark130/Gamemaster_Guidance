"""Defines the GGJob class."""

# Standard Imports
from typing import Any, Final, List
# Third Party Imports
# Local Imports
from gamemaster_guidance.gg_globals import FUNC_SPECIAL_LIST
from gamemaster_guidance.gg_misc import validate_num, validate_percent, validate_scale
from gamemaster_guidance.gg_rando import rand_list_entry
import gamemaster_guidance.gg_globals as GG_GLOBALS  # For brevity


# A list of non-"score" jobs (that still need to get done)
_JOB_GUARD: Final[str] = 'guard duty'    # Door guard, "vault" supervisor, bar liaison
_JOB_PATROL: Final[str] = 'patrol'       # Patrol the guild's territory
_JOB_INVEST: Final[str] = 'investigate'  # Investigate a potential customer, ally, mark, etc
_JOB_RECRUIT: Final[str] = 'recruit'     # Recruit new members into the gang
_JOB_ESCORT: Final[str] = 'escort'       # Escort guild member, customer, ally, etc for safety
_JOB_EXPAND: Final[str] = 'expansion'    # Gang/guild war; aggressive expansion of territory
_JOB_LIST: Final[List] = sorted([_JOB_GUARD, _JOB_PATROL, _JOB_INVEST, _JOB_RECRUIT, _JOB_ESCORT,
                                 _JOB_EXPAND])
# Some functional specialties require different "formulas" to generate scores.  Those functional
# specialties are listed here.
_PROPERTY_SHOPLIFT: Final[str] = 'shoplifting'
_PROPERTY_PICKPOCKET: Final[str] = 'pick-pocketing'
_PROPERTY_VANDAL: Final[str] = 'vandalism'
_PROPERTY_ARSON: Final[str] = 'arson'
_PROPERTY_BURGLARY: Final[str] = 'burglary'
_PROPERTY_FENCE: Final[str] = 'fencing'
_FUNC_SPEC_LOOKUP: Final[dict] = {
    # GG_GLOBALS.FUNC_SPECIAL_CORRUPTION: [],
    # GG_GLOBALS.FUNC_SPECIAL_COUNTERFEIT: [],
    # GG_GLOBALS.FUNC_SPECIAL_DRUGS: [],
    # GG_GLOBALS.FUNC_SPECIAL_EXPLOIT: [],
    # GG_GLOBALS.FUNC_SPECIAL_FRAUD: [],
    GG_GLOBALS.FUNC_SPECIAL_PROPERTY:
        ([_PROPERTY_BURGLARY] * 6)
        + ([_PROPERTY_FENCE] * 5)
        + ([_PROPERTY_PICKPOCKET] * 2)
        + ([_PROPERTY_SHOPLIFT] * 2)
        + ([_PROPERTY_ARSON] * 2)
        + ([_PROPERTY_VANDAL] * 1),
    # GG_GLOBALS.FUNC_SPECIAL_RACKET: [],
    # GG_GLOBALS.FUNC_SPECIAL_SMUGGLE: [],
    # GG_GLOBALS.FUNC_SPECIAL_VICE: [],
    # GG_GLOBALS.FUNC_SPECIAL_VIOLENCE: []
    }


class GGJob():
    """Generate one or more jobs based on functional specialties."""

    def __init__(self, special_dict: dict = None, goals: Any = 1, territory: Any = 1) -> None:
        """Class ctor.

        Args:
            special_dict: [Optional] Expects FUNC_SPECIAL_LIST entries as keys and %s as values.
                Can be None.  If None, the class will assume an equal distribution across the
                functional specialties.
            goals: [Optional] On a scale of 1 to 10, 1 being isolationist and 10 being expansionist,
                how prevalent do you want 'expansion' jobs to be?  Value can be an int or float.
            territory: [Optional] On a scale of 1 to 10, 1 being beneath notice and 10 being most
                of the city, how prevalent do you want 'patrol' jobs to be?  Value can be an int
                or float.
        """
        self._special_dict = special_dict  # Input dictionary
        self._goals = goals                # Isolationism-to-expansionist scale affects 'expansion'
        self._territory = territory        # Nothing-to-city scale affects 'patrol' jobs
        self._validated = False            # Controls internal validation
        self._job_cat_list = []            # Contains special_dict and _JOB_LIST entries

    ##################
    # PUBLIC METHODS #
    ##################
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

    ###################
    # PRIVATE METHODS #
    ###################
    # Organized alphabetically

    def _prepare_job_cat_list(self) -> None:
        """Populate the _job_cat_list if it hasn't been done already."""
        if not self._job_cat_list:
            self._job_cat_list = []  # Just in case it's not a list...
            # Populate with "scores" from self._special_dict
            for entry, count in self._special_dict.items():
                for _ in range(count):
                    self._job_cat_list.append(entry)
            # Populate with "jobs" from _JOB_LIST
            # Flat entries
            for _ in range(10):
                self._job_cat_list.append(_JOB_GUARD)
                self._job_cat_list.append(_JOB_INVEST)
                self._job_cat_list.append(_JOB_RECRUIT)
                self._job_cat_list.append(_JOB_ESCORT)
            # Goals
            for _ in range(round(10 * self._goals)):
                self._job_cat_list.append(_JOB_EXPAND)
            # Territory
            for _ in range(round(10 * self._territory)):
                self._job_cat_list.append(_JOB_PATROL)

    def _rando_guild_job_details(self, category: str) -> str:
        """Randomize job details based on guild work to be done.

        Args:
            category: A string from _JOB_LIST.
        """
        # LOCAL VARIABLES
        job_details = ''  # Job details
        # Method name lookup dictionary for guild jobs.  Each must return a string.
        func_lookup = {
            _JOB_GUARD: self._rando_guild_job_details_guard,
            _JOB_PATROL: self._rando_guild_job_details_patrol,
            _JOB_INVEST: self._rando_guild_job_details_invest,
            _JOB_RECRUIT: self._rando_guild_job_details_recruit,
            _JOB_ESCORT: self._rando_guild_job_details_escort,
            _JOB_EXPAND: self._rando_guild_job_details_expand,
        }

        # INPUT VALIDATION
        if category not in _JOB_LIST:
            raise RuntimeError(f'Unknown guild job category: {category}')
        if category not in func_lookup:
            raise RuntimeError(f'Unsupported guild job category: {category}')

        # RANDO IT
        job_details = func_lookup[category]()

        # DONE
        return job_details

    def _rando_guild_job_details_guard(self) -> str:
        """Randomize a specific guild job that falls into the 'guard duty' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_guild_job_details_patrol(self) -> str:
        """Randomize a specific guild job that falls into the 'patrol' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_guild_job_details_invest(self) -> str:
        """Randomize a specific guild job that falls into the 'investigate' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_guild_job_details_recruit(self) -> str:
        """Randomize a specific guild job that falls into the 'recruitment' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_guild_job_details_escort(self) -> str:
        """Randomize a specific guild job that falls into the 'escort' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_guild_job_details_expand(self) -> str:
        """Randomize a specific guild job that falls into the 'aggressive expansion' category."""
        # LOCAL VARIABLES
        job_details = ''  # Details about this guild job

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return job_details

    def _rando_job(self) -> str:
        """Randomize one job."""
        # LOCAL VARIABLES
        job_cat = ''      # Type of job to randomize specifics for
        job_details = ''  # Description of the specific job

        # RANDO IT
        # Prepare selection list
        self._prepare_job_cat_list()
        # Randomize a category of job
        job_cat = rand_list_entry(choices=self._job_cat_list)
        # Randomize the specific job
        job_details = self._rando_job_details(category=job_cat)

        # DONE
        return job_details

    def _rando_job_details(self, category: str) -> str:
        """Randomize job details for a specific job category.

        Args:
            category: This string must be found in FUNC_SPECIAL_LIST or _JOB_LIST.
        """
        # LOCAL VARIABLES
        job_details = ''  # Job details

        # RANDO IT
        if category in FUNC_SPECIAL_LIST:
            job_details = self._rando_score_details(specialty=category)
        elif category in _JOB_LIST:
            job_details = self._rando_guild_job_details(category=category)
        else:
            raise RuntimeError(f'Unsupported job category: {category}')

        # DONE
        return job_details

    def _rando_score_details(self, specialty: str) -> str:
        """Randomize score details based on a given functional speciality.

        Args:
            specialty: A string from FUNC_SPECIAL_LIST.
        """
        # LOCAL VARIABLES
        score_details = ''    # Details of the specialty score
        # Method name lookup dictionary for functional specialties.  Each must return a string.
        func_lookup = {
            GG_GLOBALS.FUNC_SPECIAL_CORRUPTION: self._rando_score_details_corrupt,
            GG_GLOBALS.FUNC_SPECIAL_COUNTERFEIT: self._rando_score_details_counter,
            GG_GLOBALS.FUNC_SPECIAL_DRUGS: self._rando_score_details_drugs,
            GG_GLOBALS.FUNC_SPECIAL_EXPLOIT: self._rando_score_details_exploit,
            GG_GLOBALS.FUNC_SPECIAL_FRAUD: self._rando_score_details_fraud,
            GG_GLOBALS.FUNC_SPECIAL_PROPERTY: self._rando_score_details_property,
            GG_GLOBALS.FUNC_SPECIAL_RACKET: self._rando_score_details_racket,
            GG_GLOBALS.FUNC_SPECIAL_SMUGGLE: self._rando_score_details_smuggle,
            GG_GLOBALS.FUNC_SPECIAL_VICE: self._rando_score_details_vice,
            GG_GLOBALS.FUNC_SPECIAL_VIOLENCE: self._rando_score_details_violence,
        }

        # INPUT VALIDATION
        if specialty not in FUNC_SPECIAL_LIST:
            raise RuntimeError(f'Unknown functional specialty: {specialty}')
        if specialty not in func_lookup:
            raise RuntimeError(f'Unsupported functional specialty: {specialty}')

        # RANDO IT
        score_details = func_lookup[specialty]()

        # DONE
        return score_details

    def _rando_score_details_corrupt(self) -> str:
        """Randomize a specific score that falls into the corruption functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_counter(self) -> str:
        """Randomize a specific score that falls into the counterfeiting functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_drugs(self) -> str:
        """Randomize a specific score that falls into the drugs functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_exploit(self) -> str:
        """Randomize a specific score that falls into the exploitation functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_fraud(self) -> str:
        """Randomize a specific score that falls into the fraud functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_property(self) -> str:
        """Randomize a specific score that falls into the property functional specialty."""
        # LOCAL VARIABLES
        sub_specialty = None  # The specific type of job available within the functional specialty
        score_details = ''    # Details about this score

        # RANDO IT
        # Is there a sub-specialty?
        try:
            sub_specialty = rand_list_entry(_FUNC_SPEC_LOOKUP[GG_GLOBALS.FUNC_SPECIAL_PROPERTY])
        except KeyError as err:
            raise RuntimeError(f'Where are the {GG_GLOBALS.FUNC_SPECIAL_PROPERTY} '
                               'sub-specialties?') from err
        # TO DO: DON'T DO NOW... switch on the sub-specialty, fill in a templated string, and return
        print(f'SUB SPECIALTY: {sub_specialty}')  # TEMP

        # DONE
        return score_details

    def _rando_score_details_racket(self) -> str:
        """Randomize a specific score that falls into the racketeering functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_smuggle(self) -> str:
        """Randomize a specific score that falls into the smuggling functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_vice(self) -> str:
        """Randomize a specific score that falls into the vice functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _rando_score_details_violence(self) -> str:
        """Randomize a specific score that falls into the violent crimes functional specialty."""
        # LOCAL VARIABLES
        score_details = ''  # Details about this score

        # RANDO IT
        # TO DO: DON'T DO NOW... fill in a templated string and return

        # DONE
        return score_details

    def _validate_input(self) -> None:
        """Validate ctor input.

        Call this method in every public method.
        """
        # INPUT VALIDATION
        if self._validated is False:
            # special_dict
            self._validate_special_dict()
            # goals
            validate_scale(self._goals, 'goals argument')
            # territory
            validate_scale(self._territory, 'territory argument')

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
