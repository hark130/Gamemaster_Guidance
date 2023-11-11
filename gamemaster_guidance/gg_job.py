"""Defines the GGJob class."""

# Standard Imports
from typing import Any, Final, List
import os
# Third Party Imports
# Local Imports
from gamemaster_guidance.gg_file_io import read_entries
from gamemaster_guidance.gg_globals import FUNC_SPECIAL_LIST
from gamemaster_guidance.gg_misc import validate_num, validate_percent, validate_scale
from gamemaster_guidance.gg_rando import rand_integer, rand_list_entry
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


# pylint: disable=too-many-instance-attributes
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
        self._func_special_list = []       # Contains just special_dict entries
        self._score_title = '[SCORE]'      # Standardized job header for scores
        self._job_title = '[JOB]'          # Standardized job header for guild jobs
        # These list are read from the file and stored in the object.  Read once, reference many.
        self._adj_list = []                # Contents of Common-Thing_Adjective.txt (if needed)
        self._person_list = []             # Contents of Common-People.txt database (if needed)
        self._thing_list = []              # Contents of Common-Thing.txt database (if needed)
        self._setting_list = []            # Contents of Common-Setting.txt database (if needed)

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

    def _get_thing_adj_list(self) -> List[str]:
        """Read the Common-Thing_Adjective.txt database and return it."""
        if not self._adj_list:
            self._adj_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                          'Common-Thing_Adjective.txt'))
        return self._adj_list

    def _prepare_job_cat_list(self) -> None:
        """Populate the _job_cat_list if it hasn't been done already."""
        if not self._job_cat_list:
            self._job_cat_list = []  # Just in case it's not a list...
            # Populate with "scores" from self._special_dict
            for entry, count in self._special_dict.items():
                for _ in range(count):
                    self._func_special_list.append(entry)
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

    def _rando_a_person(self) -> str:
        """Randomize one person from the Common-People.txt database."""
        # VALIDATION
        if not self._person_list:
            self._person_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                             'Common-People.txt'))
        # RANDO IT
        return rand_list_entry(self._person_list)

    def _rando_a_setting(self) -> str:
        """Randomize one person from the Common-Setting.txt database."""
        if not self._setting_list:
            self._setting_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                              'Common-Setting.txt'))
        # RANDO IT
        return rand_list_entry(self._setting_list)

    def _rando_a_thing(self) -> str:
        """Randomize one person from the Common-Thing.txt database."""
        if not self._thing_list:
            self._thing_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                            'Common-Thing.txt'))
        # RANDO IT
        return rand_list_entry(self._thing_list)

    def _rando_common_details(self, preamble: str, verb_list: List[str],
                              adj_list: List[str] = None) -> str:
        """Randomize some common details using unique verbs and optional adjectives.

        Many of the job/score detail results followed the same formula.  This method will help
        make the randomization job easier.  This method will return a string that conforms to the
        following format:

            '<preamble><Person> wants the guild to <verb> a(n) <adjective> <thing> which is owned
             by a(n) <person>'

        Args:
            preamble: A string to preprend to the return value.  Could be empty.
            verb_list: A list of verbs to randomize from.
            adj_list: [Optional] A list of adjectives to apply to the 'thing'.  An adjective will
                be ommitted if the list empty or the value is None.
        """
        # LOCAL VARIABLES
        details = preamble                 # Build the common details as it goes
        customer = self._rando_a_person()  # The customer
        owner = self._rando_a_person()     # The owner of the thing
        verb = rand_list_entry(verb_list)  # What the customer wants the guild to do
        adjective = ''                     # The adjective describing the thing
        thing = self._rando_a_thing()      # The thing

        # PREPARE
        if isinstance(adj_list, list) and adj_list:
            adjective = rand_list_entry(adj_list) + ' '  # Leave a space to make formatting easier

        # RANDO IT
        details = details + f'{customer.capitalize()} wants the guild to ' \
            + f'{verb.lower()} a(n) {adjective.lower()}{thing.lower()} which ' \
            + f'is owned by a(n) {owner.lower()}'

        # DONE
        return details

    def _rando_uncommon_details(self, preamble: str, verb_list: List[str],
                                person_list: List[str]) -> str:
        """Randomize some uncommon details using unique verbs.

        Some of the job/score detail resulted in this particular formula.  This method will help
        make that randomization job easier.  This method will return a string that conforms to the
        following format:

            '<preamble>The guild needs you to <verb> a/the <person> in <setting>'

        Args:
            preamble: A string to preprend to the return value.  Could be empty.
            verb_list: A list of verbs to randomize from.
            person_list: A list of people to randomize from.
        """
        # LOCAL VARIABLES
        details = preamble                     # Build the common details as it goes
        verb = rand_list_entry(verb_list)      # What the customer wants the guild to do
        person = rand_list_entry(person_list)  # Who needs to be "verbed"?
        setting = self._rando_a_setting()      # Where will it take place?

        # RANDO IT
        details = details + f'The guild needs you to {verb} a/the {person} in/near a(n) {setting}'

        # DONE
        return details

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

    def _rando_guild_job_details_escort(self) -> str:
        """Randomize a specific guild job that falls into the 'escort' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_ESCORT.title()} - '  # Details about this guild job
        # List of related verbs
        verb_list = ['follow', 'guard', 'loosely follow', 'scout for', 'closely follow',
                     'accompany', 'stick to', 'observe']
        # List of potential escortees
        escortee_list = ['the Guildmaster', 'one Underboss', 'two Underbosses', 'one master thief'
                         f'{rand_integer(2, 3)} master thieves', 'one guild thief',
                         f'{rand_integer(3, 5)} guild thieves', 'one guild sneak',
                         f'{rand_integer(5, 9)} guild sneaks', 'one new recruit',
                         f'{rand_integer(9, 13)} new recruits', "the guild's patron",
                         "the guild's customer", "the guild's ally",
                         "the guild's contact", "a guild-affiliated contractor"]
        # List of destination types
        type_list = ['meeting', 'pickup', 'training', 'public event', 'field observation',
                     'deal', 'negotiation', 'transaction', 'drop off', 'dead drop']
        # Geographic locations
        setting = self._rando_a_setting()

        # RANDO IT
        job_details = job_details + f'{rand_list_entry(verb_list).capitalize()} ' \
            + f'{rand_list_entry(escortee_list)} to a {rand_list_entry(type_list)} ' \
            + f'at a(n) {setting}'

        # DONE
        return job_details

    def _rando_guild_job_details_expand(self) -> str:
        """Randomize a specific guild job that falls into the 'aggressive expansion' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_EXPAND.title()} - '  # Details about this guild job
        # List of related verbs
        verb_list = ['hit', 'accost', 'chase', 'distract', 'annoy', 'pester', 'attack', 'wound',
                     'hurt', 'kill', 'hamper', 'stop', 'hinder', 'halt', 'delay', 'waylay',
                     'ambush', 'kidnap', 'question', 'exile', 'intimidate', 'imprison']
        # A list of target's susceptible to expansion
        target_list = ["a competitor's gang", 'a local gang', "another guild's members",
                       "an enemy's vault", 'an opposing guild', "an enemy's guildhall",
                       "an opposing guild's affiliated gang", "an opposing gang's customer",
                       "an opposing guild's customer", "an opposing gang's patron",
                       "an opposing guild's patron", "an opposing gang's ally",
                       "an opposing guild's ally", "an enemy's warehouse", "another guild's patrol",
                       "another guild's thieves"]

        # RANDO IT
        job_details = job_details + f'{rand_list_entry(verb_list).capitalize()} ' \
            + f'{rand_list_entry(target_list)}'

        # DONE
        return job_details

    def _rando_guild_job_details_guard(self) -> str:
        """Randomize a specific guild job that falls into the 'guard duty' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_GUARD.title()} - '  # Details about this guild job
        # Various guard duty responsibilities
        duties = ['backdoor guard', 'warehouse guard', 'vault supervisor', 'bar liaison',
                  'prison guard']
        duty = rand_list_entry(duties)  # Random duty

        # RANDO IT
        job_details = job_details + f'{duty.capitalize()}'
        if 'prison' in duty:
            job_details = job_details + f' for {rand_integer(3, 10)} prisoners'
        else:
            job_details = job_details + ' for 12 hours'

        # DONE
        return job_details

    def _rando_guild_job_details_invest(self) -> str:
        """Randomize a specific guild job that falls into the 'investigate' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_INVEST.title()} - '  # Details about this guild job
        # List of relationships
        relation_list = ['patron', 'customer', 'ally', 'contact', 'contractor', 'mark']
        # Relationship descriptors
        adj_list = ['potential', 'former', 'current', 'prospective', "enemy's", "ally's",
                    "employer's"]

        # RANDO IT
        job_details = job_details + f'Observe and report on a(n) {rand_list_entry(adj_list)} ' \
            + f'{rand_list_entry(relation_list)}'

        # DONE
        return job_details

    def _rando_guild_job_details_patrol(self) -> str:
        """Randomize a specific guild job that falls into the 'patrol' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_PATROL.title()} - '  # Details about this guild job
        # List of adjectives to describe how they should be patrolling
        adverb_list = ['quietly', 'randomly', 'silently', 'brazenly', 'softly', 'unnoticeably',
                       'invisibly', 'conspicuously', 'inconspicuously', 'prominently',
                       'noticeably', 'discretely', 'unobtrusively', 'imperceptibly']
        # List of various patrol activities
        patrol_list = ['watch thru traffic', 'inspect shipments', 'question passerbys',
                       'search for suspicious characters that pass', 'go door to door',
                       'follow law enforcement', 'observe pedestrian traffic',
                       'shadow law enforcement', 'follow large shipments', 'shadow large groups',
                       'follow large groups', 'follow suspicious people',
                       'question suspicious pedestrians']
        # List of territory locations to patrol
        location_list = ['near the guildhall', 'near the gang bar', 'around the territory border',
                         'just outside territory boundaries', 'within guild territory',
                         'in major thoroughfares through guild territory',
                         'in random guild territory locations', 'near the territory border',
                         "near the guild's warehouse", "near the guildhall's backdoor",
                         'in front of the guildhall']

        # RANDO IT
        job_details = job_details + f'{rand_list_entry(adverb_list).capitalize()} ' \
            + f'{rand_list_entry(patrol_list)} {rand_list_entry(location_list)}'

        # DONE
        return job_details

    def _rando_guild_job_details_recruit(self) -> str:
        """Randomize a specific guild job that falls into the 'recruitment' category."""
        # LOCAL VARIABLES
        job_details = f'{self._job_title}: {_JOB_RECRUIT.title()} - '  # Details about this job

        # RANDO IT
        job_details = job_details + 'Recruit someone good at ' \
            + f'{rand_list_entry(self._func_special_list)}'

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
        # Method name lookup dictionary for functional specialties.  Each must return a string.
        func_lookup = {
            _PROPERTY_SHOPLIFT: self._rando_score_details_property_shop,
            _PROPERTY_PICKPOCKET: self._rando_score_details_property_pick,
            _PROPERTY_VANDAL: self._rando_score_details_property_vandal,
            _PROPERTY_ARSON: self._rando_score_details_property_arson,
            _PROPERTY_BURGLARY: self._rando_score_details_property_burgle,
            _PROPERTY_FENCE: self._rando_score_details_property_fence,
        }

        # RANDO IT
        # Is there a sub-specialty?
        try:
            sub_specialty = rand_list_entry(_FUNC_SPEC_LOOKUP[GG_GLOBALS.FUNC_SPECIAL_PROPERTY])
        except KeyError as err:
            raise RuntimeError(f'Where are the {GG_GLOBALS.FUNC_SPECIAL_PROPERTY} '
                               'sub-specialties?') from err

        # VALIDATION
        if sub_specialty not in func_lookup:
            raise RuntimeError(f'Unsupported property crimes sub-specialty: {sub_specialty}')

        # RANDO IT
        score_details = func_lookup[sub_specialty]()

        # DONE
        return score_details

    def _rando_score_details_property_arson(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty arson."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_ARSON.capitalize()} - '
        # List of arson-related verbs
        verb_list = ['burn', 'char', 'singe', 'incinerate', 'torch', 'heat', 'ignite', 'melt',
                     'scorch', 'smolder', 'cauterize', 'cremate', 'roast', 'scald', 'toast']
        # Adjectives describing why maybe the thing is worth burning
        adjective_list = self._get_thing_adj_list()

        # RANDO IT
        score_details = self._rando_common_details(preamble=score_details, verb_list=verb_list,
                                                   adj_list=adjective_list)

        # DONE
        return score_details

    def _rando_score_details_property_burgle(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty burglary."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_BURGLARY.capitalize()} - '
        # List of arson-related verbs
        verb_list = ['steal', 'burgle', 'plunder', 'rifle', 'ransack', 'rob', 'loot',
                     'abscond with', 'liberate', 'acquire']
        # Adjectives describing why maybe the thing is worth burning
        adjective_list = self._get_thing_adj_list()

        # RANDO IT
        score_details = self._rando_common_details(preamble=score_details, verb_list=verb_list,
                                                   adj_list=adjective_list)

        # DONE
        return score_details

    def _rando_score_details_property_fence(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty fencing."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_FENCE.capitalize()} - '
        verb_list = ['buy', 'sell', 'fence', 'deliver', 'negotate for']  # List of fencing verbs
        thing = self._rando_a_thing()                                    # What is it?
        thing_adj = rand_list_entry(self._get_thing_adj_list())          # Why is the thing special?
        person = self._rando_a_person()                                  # Who is the other party?
        setting = self._rando_a_setting()                                # Where will it take place?

        # RANDO IT
        score_details = score_details + f'{rand_list_entry(verb_list).capitalize()} a(n) ' \
            + f'{thing_adj.lower()} {thing.lower()} to/from a(n) {person.lower()} ' \
            + f'at a(n) {setting.lower()}'

        # DONE
        return score_details

    def _rando_score_details_property_pick(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty pick-pocketing."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_PICKPOCKET.capitalize()} - '
        # Verbs related to pick-pocketing
        verb_list = ['distract', 'accost', 'trick', 'lure', 'assist', 'watch', 'stop', 'attack',
                     'assault', 'ambush', 'kill']
        # People that might need to be "verbed"
        person_list = ['law enforcement', 'shop keep', 'merchant', 'street vendor', 'local guards',
                       'private security', 'local gang members', 'opposing guild members', 'mage',
                       'magic user', 'witch', 'sorcerer', 'priest']

        # RANDO IT
        score_details = self._rando_uncommon_details(preamble=score_details, verb_list=verb_list,
                                                     person_list=person_list)

        # DONE
        return score_details

    def _rando_score_details_property_shop(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty shoplifting."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_SHOPLIFT.capitalize()} - '
        # Verbs related to shoplifting
        verb_list = ['distract', 'accost', 'trick', 'lure', 'assist', 'watch', 'stop', 'attack',
                     'assault', 'ambush', 'kill']
        # People that might need to be "verbed"
        person_list = ['law enforcement', 'shop keep', 'merchant', 'street vendor', 'local guards',
                       'private security', 'local gang members', 'opposing guild members', 'mage',
                       'magic user', 'witch', 'sorcerer', 'priest']

        # RANDO IT
        score_details = self._rando_uncommon_details(preamble=score_details, verb_list=verb_list,
                                                     person_list=person_list)

        # DONE
        return score_details

    def _rando_score_details_property_vandal(self) -> str:
        """Randomize a score that falls into the property crime sub-specialty vandalism."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_PROPERTY.upper()} - ' \
                        f'{_PROPERTY_VANDAL.capitalize()} - '
        # List of vandalism-related verbs
        verb_list = ['bend', 'break', 'chip', 'scrape', 'scratch', 'deface', 'desecrate', 'paint',
                     'cut', 'gouge', 'scratch up', 'scrape up', 'crack']
        # Adjectives describing why maybe the thing is worth vandalizing
        adjective_list = self._get_thing_adj_list()

        # RANDO IT
        score_details = self._rando_common_details(preamble=score_details, verb_list=verb_list,
                                                   adj_list=adjective_list)

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
