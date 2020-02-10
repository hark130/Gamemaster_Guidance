# Standard Imports
import random

# Third Party Imports


# Local Imports
from . GG_Character import GG_Character
from . GG_Globals import print_header


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
        self._class = None  # Bounty's character class
        self._level = None  # Bounty's character level

        self._create_bounty()

    def _create_bounty(self):
        # Level
        (self._class, self._level) = self.cityObj.rando_npc_class_level()
        # Wanted Status
        self._rando_wanted_status()
        # Complications
        self._rando_reward()

    def _rando_reward(self):
        self._reward = 0

    def _rando_wanted_status(self):
        self._wanted_status = random.choice(self.supportedStates)

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
        self.print_bounty_level()

    def print_gm_details(self):
        print_header("GM Details")
        self.print_notes()
        self.print_traits()

    def print_all_details(self):
        print_header("BOUNTY DETAILS")
        self.print_public_details()
        self.print_private_details()
        self.print_gm_details()

    def print_reward(self):
        """Print the bounty's reward"""
        self._print_something("Reward:", str(self._reward))

    def print_wanted_status(self):
        """Print the bounty's wanted status"""
        self._print_something("Wanted:", self._wanted_status)

    def print_bounty_class(self):
        """Print the bounty's character class"""
        self._print_something("Class:", self._class)

    def print_bounty_level(self):
        """Print the bounty's character level"""
        self._print_something("Level:", self._level)
