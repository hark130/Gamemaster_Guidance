from GG_File_IO import pick_entry
from GG_Rando import rand_percent

import os
import random


class GG_Ancestry:
    supportedAncestry = ["Dwarf", "Elf", "Gnome", "Goblin", "Halfling"]
    genderList = ["Male", "Female"]


    def __init__(self, race=None, sex=None):
        """Class constructor"""

        # Ancestry
        if race and race not in self.supportedAncestry:
            raise RuntimeError("Unsupported race")
        elif race:
            self.ancestry = race
        else:
            self._rando_ancestry()

        # Gender
        if sex and sex not in self.genderList:
            raise RuntimeError("Unsupported sex")
        if sex:
            self.gender = sex
        else:
            self._rando_gender()

        # Name
        self._rando_name()


    def return_full_name(self):
        return self.fullName


    def return_race(self):
        return self.ancestry


    def return_sex(self):
        return self.gender


    def _rando_ancestry(self):
        """Initialize the ancestry attribute"""
        self.ancestry = random.choice(self.supportedAncestry)


    def _rando_gender(self):
        """Initialize the gender attribute"""
        if rand_percent() < 51:
            self.gender = self.genderList[0]
        else:
            self.gender = self.genderList[1]        


    def _rando_name(self):
        self._rando_given_name()
        self._rando_surname()
        self.fullName = "%s %s" % (self.givenName, self.surname)


    def _rando_given_name(self):
        if self.ancestry is "Gnome" or self.ancestry is "Goblin":
            self.givenName = self._get_default_given_name()
        elif self.gender is self.genderList[0]:
            self._rando_male_given_name()
        else:
            self._rando_female_given_name()


    def _rando_male_given_name(self):
        self.givenName = self._get_male_given_name()


    def _get_default_given_name(self):
        dbName = "Names-" + self.ancestry + "-Given_Name.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _get_male_given_name(self):
        dbName = "Names-" + self.ancestry + "-Given_Name-Male.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_female_given_name(self):
        dbName = "Names-" + self.ancestry + "-Given_Name-Female.txt"
        self.givenName = pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_surname(self):
        if self.ancestry is "Elf":
            self._rando_elf_surname()
        elif self.ancestry is "Dwarf":
            self._rando_dwarf_surname()
        elif self.ancestry is "Gnome" or self.ancestry is "Goblin":
            self.surname = ""
        else:
            self.surname = self._get_default_surname()


    def _rando_elf_surname(self):
        elvenSurname = "%s of %s"
        # Relationship
        if self.gender is self.genderList[0]:
            relationship = "son"
        else:
            relationship = "daughter"
        # Father's name
        father = self.givenName
        while father is self.givenName:
            father = self._get_male_given_name()

        self.surname = elvenSurname % (relationship, father)


    def _rando_dwarf_surname(self):
        dwarfSurname = "of %s"
        dwarfClan = self._get_default_surname()
        self.surname = dwarfSurname % (dwarfClan)


    def _get_default_surname(self):
        dbName = "Names-" + self.ancestry + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))
