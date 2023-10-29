# Standard
import os
# Third Party
# Local
from gamemaster_guidance.gg_ancestry import GGAncestry
from gamemaster_guidance.gg_file_io import pick_entries


class GGCharacter:
    """Create and print a new character"""
    entryTitleWidth = 10  # Width of each printed entry's title
    entryFormatStr = "{:"+str(entryTitleWidth)+"}"

    def __init__(self, race=None, sex=None, num_traits=3, city_object=None):
        """Class constructor"""
        # City Stats
        self.city_obj = city_object
        if self.city_obj and not race:
            self.city_obj.load()
            race = self.city_obj.rando_city_race()

        # Ancestry
        self.charAncestry = GGAncestry(race, sex, city_object)
        # Traits
        dbFilename = os.path.join(os.getcwd(), "databases", "Traits.txt")
        self.traitList = pick_entries(dbFilename, num_traits)


    def print_character(self):
        """Print all character descriptions"""
        print("\n")
        self.print_name()
        self.print_race()
        self.print_sex()
        self.print_notes()
        self.print_traits()
        print("\n")


    def print_name(self):
        """Print the character's full name"""
        self._print_something("Name:", self.charAncestry.return_full_name())


    def print_race(self):
        """Print the character's race"""
        charEthnicity = self.charAncestry.return_ethnicity()
        charSubGroup = self.charAncestry.return_subgroup()

        self._print_something("Race:", self.charAncestry.return_race())

        if charEthnicity:
            self._print_something("Ethnicity:", charEthnicity)

        if charSubGroup:
            self._print_something("Subgroup:", charSubGroup)


    def print_sex(self):
        """Print the character's gender"""
        self._print_something("Gender:", self.charAncestry.return_sex())


    def print_notes(self):
        """Print the character's notes"""
        # LOCAL VARIABLES
        charNotes = self.charAncestry.return_notes()
        listOfNotes = []

        # PARSE NOTES
        if isinstance(charNotes, list):
            listOfNotes = charNotes
        elif isinstance(charNotes, str):
            listOfNotes.append(charNotes)
        else:
            try:
                listOfNotes.append(str(charNotes))
            except:
                listOfNotes = None

        # PRINT NOTES
        if listOfNotes:
            if len(listOfNotes) == 1:
                self._print_something("Note:", listOfNotes[0])
            else:
                self._print_something("Notes:", "")
                for note in listOfNotes:
                    self._print_something("", note)


    def print_traits(self):
        """Print the character's traits"""
        self._print_something("Traits:", "")
        for trait in self.traitList:
            self._print_something("", trait)


    def _print_something(self, title, entry):
        """Standardize the format on behalf of all print_* methods"""
        print(self.entryFormatStr.format(title) + " " + entry)
