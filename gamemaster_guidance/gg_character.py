"""Defines the GGCharacter class to create and print new characters."""

# Standard
import os
# Third Party
# Local
from gamemaster_guidance.gg_ancestry import GGAncestry
from gamemaster_guidance.gg_file_io import pick_entries


class GGCharacter:
    """Create and print a new character"""
    entry_title_width = 10  # Width of each printed entry's title
    entry_format_str = "{:"+str(entry_title_width)+"}"

    def __init__(self, race=None, sex=None, num_traits=3, city_object=None):
        """Class constructor"""
        # City Stats
        self.city_obj = city_object
        if self.city_obj and not race:
            self.city_obj.load()
            race = self.city_obj.rando_city_race()

        # Ancestry
        self.char_ancestry = GGAncestry(race, sex, city_object)
        # Traits
        db_filename = os.path.join(os.getcwd(), "databases", "Traits.txt")
        self.trait_list = pick_entries(db_filename, num_traits)

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
        self._print_something("Name:", self.char_ancestry.return_full_name())

    def print_race(self):
        """Print the character's race"""
        char_ethnicity = self.char_ancestry.return_ethnicity()
        char_sub_group = self.char_ancestry.return_subgroup()

        self._print_something("Race:", self.char_ancestry.return_race())

        if char_ethnicity:
            self._print_something("Ethnicity:", char_ethnicity)

        if char_sub_group:
            self._print_something("Subgroup:", char_sub_group)

    def print_sex(self):
        """Print the character's gender"""
        self._print_something("Gender:", self.char_ancestry.return_sex())

    def print_notes(self):
        """Print the character's notes"""
        # LOCAL VARIABLES
        char_notes = self.char_ancestry.return_notes()
        list_of_notes = []

        # PARSE NOTES
        if isinstance(char_notes, list):
            list_of_notes = char_notes
        elif isinstance(char_notes, str):
            list_of_notes.append(char_notes)
        else:
            list_of_notes.append(str(char_notes))

        # PRINT NOTES
        if list_of_notes:
            if len(list_of_notes) == 1:
                self._print_something("Note:", list_of_notes[0])
            else:
                self._print_something("Notes:", "")
                for note in list_of_notes:
                    self._print_something("", note)

    def print_traits(self):
        """Print the character's traits"""
        self._print_something("Traits:", "")
        for trait in self.trait_list:
            self._print_something("", trait)

    def _print_something(self, title, entry):
        """Standardize the format on behalf of all print_* methods"""
        print(self.entry_format_str.format(title) + " " + entry)
