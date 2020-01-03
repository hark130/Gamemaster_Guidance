import os

from GG_Ancestry import GG_Ancestry
from GG_File_IO import pick_entries


class GG_Character:
    entryTitleWidth = 10  # Width of each printed entry's title
    entryFormatStr = "{:"+str(entryTitleWidth)+"}"

    def __init__(self, race=None, sex=None, numTraits=3):
        """Class constructor"""
        # Ancestry
        self.charAncestry = GG_Ancestry(race, sex)
        # Traits
        dbFilename = os.path.join(os.getcwd(), "databases", "Traits.txt")
        self.traitList = pick_entries(dbFilename, numTraits)


    def print_character(self):
        print("\n")
        self.print_name()
        self.print_race()
        self.print_sex()
        self.print_traits()
        print("\n")


    def print_name(self):
        self._print_something("Name:", self.charAncestry.return_full_name())


    def print_race(self):
        self._print_something("Race:", self.charAncestry.return_race())


    def print_sex(self):
        self._print_something("Gender:", self.charAncestry.return_sex())


    def print_traits(self):
        self._print_something("Traits:", "")
        for trait in self.traitList:
            self._print_something("", trait)
            # print("\t%s" % trait)

    def _print_something(self, title, entry):
        print(self.entryFormatStr.format(title) + " " + entry)


def main():
    testCharacter = GG_Character()
    testCharacter.print_character()


if __name__ == "__main__":
    main()
