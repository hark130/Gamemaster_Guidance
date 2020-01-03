import os

from GG_Ancestry import GG_Ancestry
from GG_File_IO import pick_entries


class GG_Character:


    def __init__(self, race=None, sex=None, numTraits=3):
        """Class constructor"""
        # Ancestry
        self.charAncestry = GG_Ancestry(race, sex)
        # Traits
        dbFilename = os.path.join(os.getcwd(), "databases", "Traits.txt")
        self.traitList = pick_entries(dbFilename, numTraits)


    def print_character(self):
        self.print_name()
        self.print_traits()


    def print_name(self):
        print(self.charAncestry.return_full_name())


    def print_traits(self):
        print("Traits:")
        for trait in self.traitList:
            print("\t%s" % trait)


def main():
    testCharacter = GG_Character()
    testCharacter.print_character()


if __name__ == "__main__":
    main()
