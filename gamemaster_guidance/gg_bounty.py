# Standard Imports
import math
import os
import random

# Third Party Imports


# Local Imports
from gamemaster_guidance.gg_character import GGCharacter
from gamemaster_guidance.gg_file_io import pick_entries
from gamemaster_guidance.gg_globals import CLASS_LIST
from gamemaster_guidance.gg_misc import print_header
from gamemaster_guidance.gg_rando import rand_integer, rand_percent


def calculate_exponential_percent(num):
    """Returns y if num were x on an exponential curve running through points (1, 10) and (20, 90)"""
    return (10 / math.pow(9, 1/19)) * math.pow(math.pow(9, 1/19), num)


class GGBounty(GGCharacter):
    """Create and print a new bounty"""

    supportedStates = ["Alive", "Dead or Alive"]
    deadRewardPercents = [.25, .5, 1]
    crimePercents = {
        1: [75,  15,  5,   5 ],
        2: [70,  17,  7,   6 ],
        3: [65,  19,  9,   7 ],
        4: [60,  21,  11,  8 ],
        5: [55,  23,  13,  9 ],
        6: [50,  25,  15,  10],
        7: [45,  27,  17,  11],
        8: [40,  29,  19,  12],
        9: [35,  31,  21,  13],
        10:[30,  33,  23,  14],
        11:[25,  33,  25,  17],
        12:[20,  31,  27,  22],
        13:[15,  29,  29,  27],
        14:[10,  27,  31,  32],
        15:[5,   25,  33,  37],
        16:[0,   23,  33,  44],
        17:[0,   21,  31,  48],
        18:[0,   19,  29,  52],
        19:[0,   17,  27,  56],
        20:[0,   15,  25,  60],
    }
    crimeDatabases = [
        os.path.join('databases', 'Crimes-00-Minor.txt'),
        os.path.join('databases', 'Crimes-01-Lesser.txt'),
        os.path.join('databases', 'Crimes-02-Serious.txt'),
        os.path.join('databases', 'Crimes-03-Severe.txt'),
    ]
    crimeTypes = ['Minor', 'Lesser', 'Serious', 'Severe']
    complicationDatabase = os.path.join('databases', 'Complications.txt')
    # {source:{probability:percent 1-100, notes:string}}
    bountySources = {
        'City guard':{
            'Probability':40,
            'Notes':'Low level crimes, guard being used as a front, or someone was bribed',
        },
        'Army':{
            'Probability':25,
            'Notes':'Escaped prison, war crimes, hated by army official, violated national law, '
            'outside city limits, or someone was bribed/enticed/influenced',
        },
        'Black Collar Union':{
            'Probability':10,
            'Notes':'Former guildsman that seriously violated the code, find a missing guildsman, '
            'murdered a guildsman, knows something about a missing/murdered guildsman, guild '
            'was bribed/enticed/influenced to front a quiet abduction, do a favor for an ally, '
            'or nab a mark at the behest of another guildhouse',
        },
        'Wealthy merchant':{
            'Probability':5,
            'Notes':'Criminal identified by police but not prioritized, front to find someone who '
            'knows something, or high-level thief'
        },
        'Nobility':{
            'Probability':5,
            'Notes':'Intrigue, sweeten the pot to locate a criminal that wronged them, find '
            'someone who knows something, bribed a magister for nefarious reasons or locate '
            'fellow nobility run away/missing/kidnapped'
        },
        'Criminal':{
            'Probability':5,
            'Notes':'Easiest way to find someone is to pay someone and then get/kill/rescue '
            'them.  Could be informant, spy, ally, or enemy.  Have someone always following the '
            'PCs.  Actual source will be a front.'
        },
        'Clergy':{
            'Probability':5,
            'Notes':'Silence a witness, find evil, find a heretic, etc.  Good way for a church '
            'to get work done without getting their hands dirty.  Source might actually be city.  '
            'Maybe have the PCs feedbly followed.'
        },
        'Magister':{
            'Probability':5,
            'Notes':'Sometimes the court needs to get to the bottom of something.  Special '
            'inquiry, official investigation, shady city guard, shady Black Jackets, etc.'
        },
    }

    def __init__(self, race=None, sex=None, numTraits=3, city_object=None, minLevel=1):
        """Class constructor"""
        # GGCharacter
        super().__init__(race, sex, numTraits, city_object)

        # GG_Bounty
        self._reward = None  # Bounty reward in gp as a str
        self._wanted_status = None  # WANTED: Dead or Alive
        self._class = None  # Bounty's character class as a str
        self._level = None  # Bounty's character level as an int
        self._crime_list = []  # List of bounty's crimes
        self._crime_type = None  # 0 - Minor, 1 - Lesser, 2 - Serious, 3 - Severe
        self._min_level = minLevel  # Minimum level
        self._complications = []  # List of potential complications to spice up the bounty
        self._bounty_source = None  # Bounty's source as a str
        assert self._min_level > 0, "Minimum level too low"
        assert self._min_level <= 20, "Minimum level too high"
        self._create_bounty()

    def _create_bounty(self):
        # Class and Level
        if self.city_obj:
            (self._class, self._level) = self.city_obj.rando_npc_class_level(self._min_level)
        else:
            self._class = random.choice(CLASS_LIST)
            self._level = rand_integer(self._min_level, 20)
        # Crime
        self._rando_crime()
        # Wanted Status
        self._rando_wanted_status()
        # Complications
        self._rando_complications()
        # Reward
        self._rando_reward()
        # Bounty Source
        self._rando_source()

    def _rando_crime(self):
        # LOCAL VARIABLES
        levelPercents = self.crimePercents[self._level]
        randoPercent = rand_percent()
        runningPercent = 0
        currIndex = -1

        # Resolve Crime
        for index in range(0,len(levelPercents)):
            runningPercent += levelPercents[index]
            if randoPercent <= runningPercent:
                currIndex = index
                self._crime_type = index
                break
        assert (currIndex > -1), 'Failed to randomize a crime'

        # Randomize Crimes
        self._crime_list = pick_entries(self.crimeDatabases[currIndex], 3)

    def _rando_wanted_status(self):
        # This equation returns (1, 10) through (20, 90)
        # Level 1 returns 10%, Level 20 returns 90%
        chanceDOA = calculate_exponential_percent(self._level)
        if rand_percent() <= chanceDOA:
            self._wanted_status = self.supportedStates[1]
        else:
            self._wanted_status = self.supportedStates[0]

    def _rando_complications(self):
        self._complications = pick_entries(self.complicationDatabase, 3)
            
    def _rando_reward(self):
        # LOCAL VARIABLES
        aliveReward = self._level * 10  # Starting point
        deadReward = ''
        splitChance = 0
        randPercent = 0
        
        # ADJUST REWARD
        # Standard Variance
        aliveReward = aliveReward * (1 + (self._crime_type * .1))
        # Complications
        # TO DO: DON'T DO NOW
        # Wanted Status
        if self._wanted_status == self.supportedStates[1]:
            # Higher the number, less of a chance for a split
            splitChance = 100 - calculate_exponential_percent(self._level)
            # Randomize a percent
            randPercent = rand_percent()
            # Determine split
            if randPercent <= splitChance:
                # Split
                if (randPercent / 2) <= splitChance:
                    deadReward = str(int(self.deadRewardPercents[0] * aliveReward))
                    self.charAncestry._add_note('A low percent dead bounty could indicate a low level or dangerous criminal.  '
                                                '(e.g., court wants to make a public example, already slated for execution, violent'
                                                ', case/criminal is generating bad press)')
                elif randPercent <= splitChance:
                    deadReward = str(int(self.deadRewardPercents[1] * aliveReward))
                    self.charAncestry._add_note('A mid percent dead bounty could indicate a dastardly or slippery felon.  '
                                                '(e.g., bad crimes, mid-to-high level')
                else:
                    # No split.  Dead bounty is the same reward as living.
                    deadReward = str(int(self.deadRewardPercents[2] * aliveReward))
                    self.charAncestry._add_note('Dead and Alive bounty rewards match.')
                    self.charAncestry._add_note('Perhaps, the mark is a nefarious or slippery villain. (e.g., egregious crimes, high level')
                    self.charAncestry._add_note('Maybe someone wants the mark permanently silenced. (e.g., innocent, knows something')
                deadReward = deadReward + '/'  # Truncate the "alive" reward later
        
        self._reward = deadReward + str(int(aliveReward))

    def _rando_source(self):
        # {source:{probability:percent 1-100, notes:string}}
        # LOCAL VARIABLES
        totalPercent = 0  # Add all the probabilities here
        randoNum = 0  # Roll

        # RANDOMIZE A SOURCE
        # 1. Add all the probabilites
        for bsValue in self.bountySources.values():
            totalPercent += bsValue["Probability"]
        # 2. Randomize a value
        if totalPercent > 1:
            randoNum = rand_integer(1, totalPercent)
        else:
            raise RuntimeError("Unable to find probabilites in the bounty source dictionary")
        # 3. Find the entry
        for (bsKey, bsValue) in self.bountySources.items():
            if randoNum <= bsValue["Probability"]:
                self._bounty_source = bsKey
                self.charAncestry._add_note("Consider... " + bsValue["Notes"])
                return
            else:
                randoNum -= bsValue["Probability"]

        raise RuntimeError("Failed to find a bounty source entry")

    def print_public_details(self):
        print_header("Public Details")
        self.print_name()
        self.print_race()
        self.print_sex()
        self.print_reward()
        self.print_wanted_status()

    def print_private_details(self):
        print_header("Private Details")
        # Known by Union
        self.print_source()
        self.print_crimes()
        # Gather Information
        self.print_bounty_class()

    def print_gm_details(self):
        print_header("GM Details")
        self.print_bounty_level()
        self.print_notes()
        self.print_traits()
        self.print_complications()

    def print_all_details(self):
        print_header("BOUNTY DETAILS")
        self.print_public_details()
        self.print_private_details()
        self.print_gm_details()

    def print_reward(self):
        """Print the bounty's reward"""
        self._print_something("Reward:", str(self._reward) + ' gp')

    def print_wanted_status(self):
        """Print the bounty's wanted status"""
        self._print_something("Wanted:", self._wanted_status)

    def print_source(self):
        """Print the source of this bounty"""
        self._print_something("Wanted By:", self._bounty_source)

    def print_bounty_class(self):
        """Print the bounty's character class"""
        self._print_something("Class:", self._class)

    def print_crimes(self):
        """Print the crimes listed for the bounty"""
        if self._crime_list:
            if len(self._crime_list) == 1:
                self._print_something("Crime:", self._crime_list[0] + f" {self.crimeTypes[self._crime_type]}")
            else:
                self._print_something("Crimes:", self.crimeTypes[self._crime_type])
                for crime in self._crime_list:
                    self._print_something("", crime)
                    
    def print_complications(self):
        """Print the complications listed for the bounty"""
        if self._complications:
            if len(self._complications) == 1:
                self._print_something("Complication:", self._complications[0])
            else:
                self._print_something("Complications:", "")
                for complication in self._complications:
                    self._print_something("", complication)

    def print_bounty_level(self):
        """Print the bounty's character level"""
        self._print_something("Level:", str(self._level))
