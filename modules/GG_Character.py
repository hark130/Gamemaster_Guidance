import os

from . GG_Ancestry import GG_Ancestry
from . GG_File_IO import pick_entries


class GG_Character:
    """Create and print a new character"""
    entryTitleWidth = 10  # Width of each printed entry's title
    entryFormatStr = "{:"+str(entryTitleWidth)+"}"

    def __init__(self, race=None, sex=None, numTraits=3, cityObj=None):
        """Class constructor"""
        # Ancestry
        self.charAncestry = GG_Ancestry(race, sex)
        # Traits
        dbFilename = os.path.join(os.getcwd(), "databases", "Traits.txt")
        self.traitList = pick_entries(dbFilename, numTraits)


    def print_character(self):
        """Print all character descriptions"""
        print("\n")
        self.print_name()
        self.print_race()
        self.print_sex()
        self.print_traits()
        print("\n")


    def print_name(self):
        """Print the character's full name"""
        self._print_something("Name:", self.charAncestry.return_full_name())


    def print_race(self):
        """Print the character's race"""
        self._print_something("Race:", self.charAncestry.return_race())


    def print_sex(self):
        """Print the character's gender"""
        self._print_something("Gender:", self.charAncestry.return_sex())


    def print_traits(self):
        """Print the character's traits"""
        self._print_something("Traits:", "")
        for trait in self.traitList:
            self._print_something("", trait)

    def _print_something(self, title, entry):
        """Standardize the format on behalf of all print_* methods"""
        print(self.entryFormatStr.format(title) + " " + entry)
