"""Defines the GGJob class."""
# pylint: disable=too-many-lines
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
_CORRUPT_GRAND: Final[str] = 'grand'  # en.wikipedia.org/wiki/Corruption#Definitions_and_scales
_CORRUPT_PETTY: Final[str] = 'petty'  # en.wikipedia.org/wiki/Corruption#Definitions_and_scales
_CORRUPT_SYSTEMIC: Final[str] = 'systemic'  # wikipedia.org/wiki/Corruption#Definitions_and_scales
_PROPERTY_ARSON: Final[str] = 'arson'
_PROPERTY_BURGLARY: Final[str] = 'burglary'
_PROPERTY_FENCE: Final[str] = 'fencing'
_PROPERTY_PICKPOCKET: Final[str] = 'pick-pocketing'
_PROPERTY_SHOPLIFT: Final[str] = 'shoplifting'
_PROPERTY_VANDAL: Final[str] = 'vandalism'
_RACKET_EXTORT: Final[str] = 'extortion'
_RACKET_LOAN: Final[str] = 'loan-sharking'
_RACKET_PROT: Final[str] = 'protection'
_FUNC_SPEC_LOOKUP: Final[dict] = {
    GG_GLOBALS.FUNC_SPECIAL_CORRUPTION:
        ([_CORRUPT_PETTY] * 3)
        + ([_CORRUPT_GRAND] * 2)
        + ([_CORRUPT_SYSTEMIC] * 1),
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
    GG_GLOBALS.FUNC_SPECIAL_RACKET:
        ([_RACKET_EXTORT] * 3)
        + ([_RACKET_PROT] * 2)
        + ([_RACKET_LOAN] * 1),
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
        self._business_list = []           # Contents of Common-Business.txt database (if needed)
        self._person_list = []             # Contents of Common-People.txt database (if needed)
        self._person_adj_list = []         # Contents of Common-People_Adjective.txt db (if needed)
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

    def _rando_a_business(self) -> str:
        """Randomize one business from the Common-Business.txt database."""
        if not self._business_list:
            self._business_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                               'Common-Business.txt'))
        # RANDO IT
        return rand_list_entry(self._business_list)

    def _rando_a_person(self, add_adj: bool = False) -> str:
        """Randomize one person from the Common-People.txt database.

        Args:
            add_adj: [Optional] Adds a random adjective from the Common-People_Adjective.txt
                database to the randomized person if True.
        """
        # LOCAL VARIABLES
        rando_person = ''  # Random person from the People database
        person_adj = ''    # Random person adjective from the People_Adjective database.

        # VALIDATION
        if add_adj and not self._person_adj_list:
            self._person_adj_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                                 'Common-People_Adjective.txt'))
        if not self._person_list:
            self._person_list = read_entries(os.path.join(os.getcwd(), 'databases',
                                             'Common-People.txt'))

        # RANDO IT
        if add_adj:
            person_adj = rand_list_entry(self._person_adj_list) + ' '
        rando_person = person_adj + rand_list_entry(self._person_list)

        # DONE
        return rando_person

    def _rando_a_public_official_high(self, add_desc: bool = True, percent_imp: int = 25) -> str:
        """Randomize a high-level public official from Japan's Edo period.

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
            percent_imp: [Optional] Percent chance, 1 - 100, to randomize a mid-level public
                official that works in the Imperial Palace.  Choosing a value of 0 will guarantee
                a high-level public official.  Conversely, choosing a value of 100 will guarantee
                a mid-level imperial public official is selected.
        """
        # LOCAL VARIABLES
        # Dictionary of high-level public officials, from Japan's Edo period, and their descriptions
        public_officials = {
            # Non-Imperial Positions
            'Shogun': 'The supreme military commander who held the highest authority.',
            'Daimyo': 'Feudal lords who governed specific territories.',
            'Hatamoto': 'Direct retainers of the Shogun, holding privileged positions. ' \
            'They were close advisors and administrators in the Shogun\'s administration.',
            'Bugyo': 'Magistrates or administrators appointed by the Shogun to oversee ' \
            'specific regions, handling legal, administrative, and financial matters.',
            'Karo': 'Chief advisors or administrators in daimyo households. They were ' \
            'influential figures, managing the daily affairs of the domain, advising the ' \
            'lord, and overseeing samurai retainers.',
            'Hanshi': 'Scholars and intellectuals who held influence by advising daimyo ' \
            'on matters related to philosophy, strategy, and governance.',
            'Metsuke': 'Officials responsible for surveillance and security, working ' \
            'under the direct authority of the shogunate. They monitored daimyo and their ' \
            'activities while residing in the capital.',
            'Machibikeshi': 'Town magistrates responsible for local governance, security, ' \
            'and enforcing laws in various towns and cities across Japan.',
            'Bugyo': 'Magistrates appointed by the shogunate to govern specific regions ' \
            'or cities. They had authority over legal, administrative, and financial matters ' \
            'within their assigned territories.',
            'Karō': 'Chief advisors or administrators in daimyo households. They were ' \
            'influential figures, managing the daily affairs of the domain, advising the ' \
            'lord, and overseeing samurai retainers.',
            'Mura-bugyō': 'Officials responsible for overseeing villages or rural areas, ' \
            'handling agricultural matters, land distribution, tax collection, and local ' \
            'disputes in the countryside.',
            'Metsuke-doshin': 'A higher-ranked police official who assisted metsuke in ' \
            'maintaining security and order. They had authority over lower-ranked constables.',
            'Kasai Jodai': 'Administrators in charge of governing Kasai, overseeing its ' \
            'economic activities, trade, and harbor operations, playing a pivotal role in ' \
            'the city\'s growth and development.',
            'Sobashu': 'Officials who managed and regulated inns, tea houses, and ' \
            'entertainment establishments. They oversaw licensing, taxation, and ' \
            'compliance with regulations in these businesses.',
            'Jisha-bugyo': 'Officials responsible for overseeing and managing shrines, ' \
            'ensuring their proper maintenance, conducting rituals, and handling ' \
            'shrine-related affairs.',
            # Imperial Positions
            'Emperor': 'The ceremonial head of state and symbol of unity for the nation. ' \
            'During the Edo Period, the Emperor held a largely ceremonial role, with actual ' \
            'political power residing in the Shogun and regional daimyo.',
            'Empress': 'The consort of the Emperor, playing significant ceremonial roles ' \
            'and responsibilities within the imperial court and contributing to cultural ' \
            'activities.',
            'Crown Prince': 'The heir to the throne, groomed for succession to the ' \
            'position of Emperor. They received education and training in governance, ' \
            'culture, and courtly duties.',
            'Grand Chamberlain': 'An official responsible for managing the Emperor\'s ' \
            'household affairs, supervising the palace staff, and overseeing ceremonies ' \
            'and audiences.',
            'Minister of the Right and Minister of the Left': 'Senior officials in the ' \
            'Daijokan (Grand Council of State) who advised the Emperor on administrative, ' \
            'legislative, and judicial matters.',
        }
        # Public official dictionary keys that count as Imperial posts
        imp_positions = ['Emperor', 'Empress', 'Crown Prince', 'Grand Chamberlain',
                         'Minister of the Right and Minister of the Left']
        important_titles = ['influential', 'high-level', 'key', 'top', 'important', 'invaluable',
                            'prominent', 'notable', 'pivotal', 'eminent', 'paramount', 'crucial',
                            'distinguished', 'vital', 'influential']
        public_official = ''  # The public official
        imp_position = False  # Indicates whether an Imperial position was selected

        # RANDO IT
        # Public Official
        if rand_integer(1, 100) <= percent_imp:
            # Imperial Public Official, mid-level
            public_official = 'Imperial ' + self._rando_a_public_official_mid(add_desc=add_desc)
            imp_position = True
        else:
            # High-level Public Official
            public_official = rand_list_entry(list(public_officials.keys()))
            if public_official in imp_positions:
                imp_position = True
            if add_desc:
                public_official = public_official \
                                  + f' ({public_officials[public_official].lower()})'
        # Are they high-level?
        if not imp_position:
            public_official = f'{rand_list_entry(important_titles)} ' + public_official

        # DONE
        return public_official

    def _rando_a_public_official_low(self, add_desc: bool = True) -> str:
        """Randomize a low-level public official from Japan's Edo period.

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
        """
        # LOCAL VARIABLES
        # Dictionary of low-level public officials, from Japan's Edo period, and their descriptions
        public_officials = {
            'Yoriki': 'Subordinate police officers or constables who assisted higher-ranking ' \
            'officials in maintaining law and order within towns or districts.',
            'Doshin': 'Police officers or town constables responsible for patrolling ' \
            'neighborhoods, enforcing curfews, and addressing minor disputes in local communities.',
            'Kurumabugyō': 'Officials responsible for overseeing transportation, especially the ' \
            'regulation and maintenance of carts, roads, and travel within a region.',
            'Yakunin': 'Lower-ranked bureaucrats or clerks assisting in administrative duties ' \
            'such as record-keeping, documentation, or managing accounts within government ' \
            'offices.',
            'Hikeshi': 'Firefighters or firemen tasked with fire prevention, emergency response, ' \
            'and firefighting duties in Edo and other major cities.',
            'Kenin': 'Servants or attendants working within the households of samurai or ' \
            'officials, often handling various domestic tasks or serving as assistants.',
            'Gokenin': 'Vassals or retainers serving under daimyo, holding lower-ranking ' \
            'positions in the feudal hierarchy and assisting in various administrative duties.',
            'Dosho': 'Medical practitioners or doctors working in local clinics or ' \
            'dispensaries, providing basic healthcare services to the public.',
            'Ninja': 'Espionage agents or covert operatives employed for intelligence ' \
            'gathering, infiltration, and other clandestine activities.',
            'Kyokan': 'Village headmen or elders responsible for local governance, resolving ' \
            'disputes, and managing community affairs in rural areas.',
            'Goyo-shu': 'Clerks or scribes responsible for maintaining records, drafting ' \
            'documents, and handling administrative tasks in local government offices.',
            'Dojo-gashira': 'Supervisors or managers overseeing public training grounds or ' \
            'martial arts schools, ensuring order and compliance with regulations.',
            'Sakaya-bugyo': 'Officials overseeing sake breweries, regulating production, ' \
            'quality, and taxation of sake, an important commodity in Japanese society.',
            'Kura-gashira': 'Administrators managing storehouses or warehouses, responsible ' \
            'for inventory, storage, and distribution of goods within a domain.',
            'Tegata-goyō': 'Bureaucrats dealing with permits or certificates required for ' \
            'various activities, such as travel permits or trade licenses.',
            "Nin'ya": 'Secretaries or assistants aiding higher-ranking officials in managing ' \
            'paperwork, correspondence, and routine administrative tasks.',
            'Shiinoki': 'Lower-level officials responsible for managing and maintaining ' \
            'government-owned forests, overseeing logging activities, and conservation efforts.',
            'Minteki-goyō': 'Officials managing or overseeing the minting and distribution ' \
            'of currency within specific regions or domains.',
            'Fudasashi': 'Couriers or messengers responsible for delivering official ' \
            'communications, documents, or orders between different administrative offices ' \
            'or regions.',
            'Kokuze-gashira': 'Administrators overseeing local land surveys, maintaining ' \
            'land records, and managing property tax assessments within a domain.',
        }
        public_official = rand_list_entry(list(public_officials.keys()))  # The public official

        # RANDO IT
        if add_desc:
            public_official = public_official + f' ({public_officials[public_official].lower()})'

        # DONE
        return public_official

    def _rando_a_public_official_mid(self, add_desc: bool = True, percent_imp: int = 25) -> str:
        """Randomize a mid-level public official from Japan's Edo period.

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
            percent_imp: [Optional] Percent chance, 1 - 100, to randomize a low-level public
                official that works in the Imperial Palace.  Choosing a value of 0 will guarantee
                a mid-level public official.  Conversely, choosing a value of 100 will guarantee
                a low-level imperial public official is selected.
        """
        # LOCAL VARIABLES
        # Dictionary of mid-level public officials, from Japan's Edo period, and their descriptions
        public_officials = {
            'Shogun': 'The supreme military commander who held the highest authority.',
            'Daimyo': 'Feudal lords who governed specific territories.',
            'Samurai': 'Warriors serving the daimyo and holding high prestige in society.',
            'Ronin': 'Masterless samurai who were often skilled swordsmen and mercenaries. ' \
            'While not public officials, they held social significance during this period.',
            'Hatamoto': 'Direct retainers of the Shogun, holding privileged positions. They ' \
            'were close advisors and administrators in the Shogun\'s administration.',
            'Metsuke': 'Officials responsible for surveillance and security, maintaining ' \
            'order and monitoring daimyo who resided there.',
            'Machibikeshi': 'Town magistrates responsible for local governance, security, ' \
            'and enforcing laws in various towns and cities.',
            'Bugyo': 'Magistrates or administrators appointed by the Shogun to oversee ' \
            'specific regions, handling legal, administrative, and financial matters.',
            'Karō': 'Chief advisors or administrators in daimyo households, managing the ' \
            'affairs of the domain and advising the lord.',
            'Hanshi': 'Scholars and intellectuals who held influence by advising daimyo on ' \
            'matters related to philosophy, strategy, and governance.',
            'Gonin-gumi Leader': 'Leaders of groups of five households, organized to ' \
            'facilitate mutual responsibility and accountability among residents.',
            'Mura-bugyo': 'Officials responsible for overseeing villages or rural areas, ' \
            'handling agricultural matters, land distribution, tax collection, and local ' \
            'disputes in the countryside.',
            'Metsuke-doshin': 'A higher-ranked police official who assisted metsuke in ' \
            'maintaining security and order within Edo. They had authority over ' \
            'lower-ranked constables.',
            'Osaka Jodai': 'Administrators in charge of governing Osaka, overseeing its ' \
            'economic activities, trade, and harbor operations, playing a pivotal role in ' \
            'the city\'s growth and development.',
            'Sobashu': 'Officials who managed and regulated inns, tea houses, and ' \
            'entertainment establishments. They oversaw licensing, taxation, and compliance ' \
            'with regulations in these businesses.',
            'Jisha-bugyo': 'Officials responsible for overseeing and managing shrines, ' \
            'ensuring their proper maintenance, conducting rituals, and handling ' \
            'shrine-related affairs.',
        }
        public_official = ''  # The public official

        # RANDO IT
        if rand_integer(1, 100) <= percent_imp:
            # Imperial Public Official, low-level
            public_official = 'Imperial ' + self._rando_a_public_official_low(add_desc=add_desc)
        else:
            # Mid-level Public Official
            public_official = rand_list_entry(list(public_officials.keys()))
            if add_desc:
                public_official = public_official \
                                  + f' ({public_officials[public_official].lower()})'

        # DONE
        return public_official

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

    def _rando_an_entity(self, add_adj: bool = False, percent_person: int = 25) -> str:
        """Randomize a random entity: person or business.

        Utilizes self._rando_a_person() and self._rando_a_business(), respectively.

        Args:
            add_adj: [Optional] Adds a random adjective from the Common-People_Adjective.txt
                database to a randomized person if True.
            percent_person: [Optional] Percent chance, 1 - 100, to randomize a person.
                The percent chance to randomize a business instead is derived from this value.
                Choosing a value of 0 will guarantee a business.  Conversely, choosing a value
                of 100 will guarantee a person is randomized.
        """
        # LOCAL VARIABLES
        target_entity = ''  # Randomized person or business

        # RANDO IT
        if rand_integer(1, 100) <= percent_person:
            # Person
            target_entity = self._rando_a_person(add_adj=add_adj)
        else:
            # Business
            target_entity = self._rando_a_business()

        # DONE
        return target_entity

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
        sub_specialty = None  # The specific type of job available within the functional specialty
        # Method name lookup dictionary for functional specialties.  Each must return a string.
        func_lookup = {
            _CORRUPT_PETTY: self._rando_score_details_corrupt_petty,
            _CORRUPT_GRAND: self._rando_score_details_corrupt_grand,
            _CORRUPT_SYSTEMIC: self._rando_score_details_corrupt_system,
        }

        # RANDO IT
        # Is there a sub-specialty?
        try:
            sub_specialty = rand_list_entry(_FUNC_SPEC_LOOKUP[GG_GLOBALS.FUNC_SPECIAL_CORRUPTION])
        except KeyError as err:
            raise RuntimeError(f'Where are the {GG_GLOBALS.FUNC_SPECIAL_CORRUPTION} '
                               'sub-specialties?') from err

        # VALIDATION
        if sub_specialty not in func_lookup:
            raise RuntimeError(f'Unsupported corruption crimes sub-specialty: {sub_specialty}')

        # RANDO IT
        score_details = func_lookup[sub_specialty]()

        # DONE
        return score_details

    def _rando_score_details_corrupt_grand(self, add_desc: bool = True) -> str:
        """Randomize a score that falls into the corruption crime sub-specialty grand.

        See: https://en.wikipedia.org/wiki/Corruption#Grand_corruption

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
        """
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_CORRUPTION.upper()} - ' \
                        f'{_CORRUPT_GRAND.capitalize()} - '
        # Ways in which a public official may be corrupted or involved with corruption
        verb_list = ['manipulate', 'bribe', 'peddle influence with', 'trade influence with',
                     'entice', 'extort', 'buy off', 'pay off', 'fix', 'induce',
                     'provide incentive to', 'motivate', 'entice', 'grease the wheels with',
                     'encourage', 'tempt']
        customer = self._rando_a_person()                                       # The customer
        public_official = self._rando_a_public_official_mid(add_desc=add_desc)  # The target

        # RANDO IT
        score_details = score_details + f'A(n) {customer.lower()} wants the guild to ' \
                        + f'{rand_list_entry(verb_list).lower()} a(n) {public_official}'

        # DONE
        return score_details

    def _rando_score_details_corrupt_petty(self, add_desc: bool = True) -> str:
        """Randomize a score that falls into the corruption crime sub-specialty petty.

        See: https://en.wikipedia.org/wiki/Corruption#Petty_corruption

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
        """
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_CORRUPTION.upper()} - ' \
                        f'{_CORRUPT_PETTY.capitalize()} - '
        # Ways in which a public official may be corrupted or involved with corruption
        verb_list = ['manipulate', 'bribe', 'peddle influence with', 'trade influence with',
                     'entice', 'extort', 'buy off', 'pay off', 'fix', 'induce',
                     'provide incentive to', 'motivate', 'entice', 'grease the wheels with',
                     'encourage', 'tempt']
        customer = self._rando_a_person()                                       # The customer
        public_official = self._rando_a_public_official_low(add_desc=add_desc)  # The target

        # RANDO IT
        score_details = score_details + f'A(n) {customer.lower()} wants the guild to ' \
                        + f'{rand_list_entry(verb_list).lower()} a(n) {public_official}'

        # DONE
        return score_details

    def _rando_score_details_corrupt_system(self, add_desc: bool = True) -> str:
        """Randomize a score that falls into the corruption crime sub-specialty systemic.

        See: https://en.wikipedia.org/wiki/Corruption#Systemic_corruption

        Args:
            add_desc: [Optional] Add the description of the Edo period public official if True.
        """
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_CORRUPTION.upper()} - ' \
                        f'{_CORRUPT_SYSTEMIC.capitalize()} - '
        # Ways in which a public official may be corrupted or involved with corruption
        verb_list = ['manipulate', 'bribe', 'peddle influence with', 'trade influence with',
                     'entice', 'extort', 'buy off', 'pay off', 'fix', 'induce',
                     'provide incentive to', 'motivate', 'entice', 'grease the wheels with',
                     'encourage', 'tempt']
        customer = self._rando_a_person()                                       # The customer
        public_official = self._rando_a_public_official_high(add_desc=add_desc)  # The target

        # RANDO IT
        score_details = score_details + f'A(n) {customer.lower()} wants the guild to ' \
                        + f'{rand_list_entry(verb_list).lower()} a(n) {public_official}'

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
        # Adjectives describing why maybe the thing is worth burgling
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
        sub_specialty = None  # The specific type of job available within the functional specialty
        # Method name lookup dictionary for functional specialties.  Each must return a string.
        func_lookup = {
            _RACKET_EXTORT: self._rando_score_details_racket_extort,
            _RACKET_LOAN: self._rando_score_details_racket_loan,
            _RACKET_PROT: self._rando_score_details_racket_prot,
        }

        # RANDO IT
        # Is there a sub-specialty?
        try:
            sub_specialty = rand_list_entry(_FUNC_SPEC_LOOKUP[GG_GLOBALS.FUNC_SPECIAL_RACKET])
        except KeyError as err:
            raise RuntimeError(f'Where are the {GG_GLOBALS.FUNC_SPECIAL_RACKET} '
                               'sub-specialties?') from err

        # VALIDATION
        if sub_specialty not in func_lookup:
            raise RuntimeError(f'Unsupported racketeering crimes sub-specialty: {sub_specialty}')

        # RANDO IT
        score_details = func_lookup[sub_specialty]()

        # DONE
        return score_details

    def _rando_score_details_racket_extort(self) -> str:
        """Randomize a score that falls into the racketeering crime sub-specialty extortion.

        <ENTITY> wants a(n) <ENTITY ADJECTIVE> <ENTITY/BUSINESS> to <EXTORTION DETAIL>
        """
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_RACKET.upper()} - ' \
                        f'{_RACKET_EXTORT.capitalize()} - '
        # Who came up with this score?
        source_entity = ['The guildmaster'] + ['The deputy guildmaster'] * 2 \
                        + ['A guild underboss'] * 3 + ['A master thief in the guild'] * 2 \
                        + ['A customer']
        target_entity = ''  # Person or business to extort for money
        # Levels of extortion
        extort_levels = ['pay a recurring flat fee'] * 10 \
                        + ['pay a regular percentage of profit'] * 4 \
                        + ['cut the guild in as a silent partner'] * 3 \
                        + ['sell the business to the guild at a discount'] * 2 \
                        + ['turn over full control to the guild'] * 1

        # RANDO IT
        target_entity = self._rando_an_entity(add_adj=True)
        score_details = score_details + f'{rand_list_entry(source_entity).capitalize()} ' \
                        + f'wants a(n) {target_entity.lower()} to ' \
                        + f'{rand_list_entry(extort_levels)}'

        # DONE
        return score_details

    def _rando_score_details_racket_loan(self) -> str:
        """Randomize a score that falls into the racketeering crime sub-specialty loan-sharking."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_RACKET.upper()} - ' \
                        f'{_RACKET_LOAN.capitalize()} - '
        # Default list of trouble-makers
        trouble_list = ['law enforcement', 'corrupt law enforcement', 'rival guild', 'local gang',
                        'vigilante/vagabond']
        # Collection list
        collect_list = [f'delinquent {self._rando_a_person()}',
                        f'{self._rando_a_person()} in hiding',
                        f'{self._rando_a_business()} business']
        shark_categories = ['protection', 'collection', 'recovery']  # Different loan-sharking jobs
        shark_category = rand_list_entry(shark_categories)           # This loan-sharking job

        # RANDO IT
        if shark_category == 'protection':
            # Protection
            score_details = score_details + 'Guild loan shark needs additional protection from ' \
                            + f'a(n) {rand_list_entry(trouble_list).lower()}'
        elif shark_category == 'collection':
            # Collection
            score_details = score_details + 'Guild loan shark needs money collected from a(n) ' \
                            + f'{rand_list_entry(collect_list).lower()}'
        elif shark_category == 'recovery':
            # Recovery
            score_details = score_details + 'Guild loan shark needs capital recovered from a(n) ' \
                            + f'{rand_list_entry(trouble_list[1:]).lower()}'
        elif shark_category not in shark_categories:
            raise RuntimeError(f'Encountered an unsupported loan-sharking job of {shark_category}')
        else:
            raise RuntimeError(f'Unimplemented loan-sharking job type of {shark_category}')

        # DONE
        return score_details

    def _rando_score_details_racket_prot(self) -> str:
        """Randomize a score that falls into the racketeering crime sub-specialty protection."""
        # LOCAL VARIABLES
        # Details about this score
        score_details = f'{self._score_title}: {GG_GLOBALS.FUNC_SPECIAL_RACKET.upper()} - ' \
                        f'{_RACKET_PROT.capitalize()} - '
        # Who came up with this score?
        source_entity = ['The guildmaster'] + ['The deputy guildmaster'] * 2 \
                        + ['A guild underboss'] * 4 + ['A guild master thief'] * 2
        # What type of client is it?
        client_type_list = ['new client', 'old client', 'unwilling client', 'willing customer']
        # Who needs protecting?
        customer = self._rando_an_entity(add_adj=True)
        # From what does the customer need to be protected?
        danger_list = ['corrupt law enforcement', 'rival guild', 'local gang', 'vagabond']

        # RANDO IT
        score_details = score_details + f'{rand_list_entry(source_entity).capitalize()} ' \
                        + f'needs a(n) {customer.lower()} ' \
                        + f'({rand_list_entry(client_type_list).lower()}) ' \
                        + f'protected from a(n) {rand_list_entry(danger_list).lower()}'

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
