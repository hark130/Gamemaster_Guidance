# Standard Imports
import math
import random

# Third Party Imports


# Local Imports
from . GG_Character import GG_Character
from . GG_Globals import print_header
from . GG_Rando import rand_percent


def calculate_exponential_percent(num):
    """Returns y if num were x on an exponential curve running through points (1, 10) and (20, 90)"""
    return (10 / math.pow(9, 1/19)) * math.pow(math.pow(9, 1/19), num)


class GG_Bounty(GG_Character):
    """Create and print a new bounty"""

    supportedStates = ["Alive", "Dead or Alive"]

    def __init__(self, race=None, sex=None, numTraits=3, cityObject=None):
        """Class constructor"""
        # GG_Character
        super().__init__(race, sex, numTraits, cityObject)

        # GG_Bounty
        self._reward = None  # Bounty reward in gp
        self._wanted_status = None  # WANTED: Dead or Alive
        self._class = None  # Bounty's character class as a str
        self._level = None  # Bounty's character level as an int

        self._create_bounty()

    def _create_bounty(self):
        # Level
        (self._class, self._level) = self.cityObj.rando_npc_class_level()
        # Wanted Status
        self._rando_wanted_status()
        # Complications
        self._rando_reward()

    def _rando_reward(self):
        self._reward = self._level * 10

    def _rando_wanted_status(self):
        # This equation returns (1, 10) through (20, 90)
        # Level 1 returns 10%, Level 20 returns 90%
        chanceDOA = calculate_exponential_percent(self._level)
        print(f'LEVEL: {self._level} % DoA: {chanceDOA}')  # DEBUGGING
        if rand_percent() <= chanceDOA:
            self._wanted_status = supportedStates[1]
        else:
            self._wanted_status = supportedStates[0]

    def print_public_details(self):
        print_header("Public Details")
        self.print_name()
        self.print_race()
        self.print_sex()
        self.print_reward()
        self.print_wanted_status()

    def print_private_details(self):
        print_header("Private Details")
        self.print_bounty_class()

    def print_gm_details(self):
        print_header("GM Details")
        self.print_bounty_level()
        self.print_notes()
        self.print_traits()

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

    def print_bounty_class(self):
        """Print the bounty's character class"""
        self._print_something("Class:", self._class)

    def print_bounty_level(self):
        """Print the bounty's character level"""
        self._print_something("Level:", str(self._level))
