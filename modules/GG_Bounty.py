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
    deadRewardPercents = [.25, .5, 1]

    def __init__(self, race=None, sex=None, numTraits=3, cityObject=None):
        """Class constructor"""
        # GG_Character
        super().__init__(race, sex, numTraits, cityObject)

        # GG_Bounty
        self._reward = None  # Bounty reward in gp as a str
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
        # LOCAL VARIABLES
        aliveReward = self._level * 10  # Starting point
        deadReward = ''
        splitChance = 0
        randPercent = 0
        
        # ADJUST REWARD
        # Standard Variance
        # TO DO: DON'T DO NOW... We don't want the PCs deciphering NPC level based on bounty reward
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
                    deadReward = str(self.deadRewardPercents[0] * aliveReward)
                    self.charAncestry._add_note('A low percent dead bounty could indicate a low level or dangerous criminal.  '
                                                '(e.g., court wants to make a public example, already slated for execution, violent'
                                                ', case/criminal is generating bad press)')
                elif randPercent <= splitChance:
                    deadReward = str(self.deadRewardPercents[1] * aliveReward)
                    self.charAncestry._add_note('A mid percent dead bounty could indicate a dastardly or slippery felon.  '
                                                '(e.g., bad crimes, mid-to-high level')
                else:
                    # No split.  Dead bounty is the same reward as living.
                    deadReward = str(self.deadRewardPercents[2] * aliveReward)
                    self.charAncestry._add_note('Dead and Alive bounty rewards match.')
                    self.charAncestry._add_note('Perhaps, the mark is a nefarious or slippery villain. (e.g., egregious crimes, high level')
                    self.charAncestry._add_note('Maybe someone wants the mark permanently silenced. (e.g., innocent, knows something')
                deadReward = deadReward + '/'  # Truncate the "alive" reward later
        
        self._reward = deadReward + str(aliveReward)

    def _rando_wanted_status(self):
        # This equation returns (1, 10) through (20, 90)
        # Level 1 returns 10%, Level 20 returns 90%
        chanceDOA = calculate_exponential_percent(self._level)
        print(f'LEVEL: {self._level} % DoA: {chanceDOA}')  # DEBUGGING
        if rand_percent() <= chanceDOA:
            self._wanted_status = self.supportedStates[1]
        else:
            self._wanted_status = self.supportedStates[0]

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
