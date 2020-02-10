# Standard Imports


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
        self._reward = 0
        self._wanted_status = None

    def print_public_details(self):
        print_header("Public Details")
        self.print_name()
        self.print_race()
        self.print_sex()

    def print_private_details(self):
        print_header("Private Details")

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
        self._print_something("Reward:", self._reward)

    def print_wanted_status(self):
        """Print the bounty's wanted status"""
        self._print_something("Wanted:", self._wanted_status)
