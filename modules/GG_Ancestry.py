from . GG_File_IO import pick_entry
from . GG_Rando import rand_percent

import os
import random


class GG_Ancestry:
    humanEthnicities = ["Garundi", "Keleshite", "Kellid", "Mwangi", "Nidalese", "Shoanti", "Taldan", "Tian", "Ulfen", "Varisian", "Vudrani"]  # User Story 8. Nidalese
    mwangiSubgroups = ["Bekyar", "Bonuwat", "Mauxi", "Zenj"]
    shoantiClans = ["Lyrune-Quah (Moon Clan)", "Shadde-Quah (Axe Clan)", "Shriikirri-Quah (Hawk Clan)",
                    "Shundar-Quah (Spire Clan)", "Sklar-Quah (Sun Clan)", "Skoan-Quah (Skull Clan)",
                    "Tamiir-Quah (Wind Clan)"]
    supportedAncestry = ["Dwarf", "Elf", "Gnome", "Goblin", "Halfling", "Human", "Half-Elf"]
    genderList = ["Male", "Female"]


    def __init__(self, race=None, sex=None):
        """Class constructor"""
        self.ethnicity = None
        self.subgroup = None
        self.notes = None

        # Ancestry
        if race and race not in self.supportedAncestry:
            raise RuntimeError("Unsupported race")
        elif race is "Human":
            self._rando_human_ethnicity()
            if self.ethnicity is "Nidalese":
                self.ethnicity = "Taldan"  # Fix this in User Story #8
            self.ancestry = race
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


    def return_ethnicity(self):
        return self.ethnicity


    def return_subgroup(self):
        return self.subgroup


    def return_sex(self):
        return self.gender


    def return_notes(self):
        return self.notes


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
        # Tian-Shu list their surname in front of their birth name.
        if self.subgroup is "Shu":
            self.fullName = "%s %s" % (self.surname, self.givenName)
        else:
            self.fullName = "%s %s" % (self.givenName, self.surname)


    def _rando_given_name(self):
        if self.ancestry is "Gnome" or self.ancestry is "Goblin":
            self.givenName = self._get_default_given_name()
        elif self.ancestry == "Half-Elf":
            self._rando_half_elf_given_name()
        elif self.gender is self.genderList[0]:
            self._rando_male_given_name()
        else:
            self._rando_female_given_name()


    def _get_default_given_name(self):
        if self.ancestry is "Human":
            dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name.txt"
        else:
            dbName = "Names-" + self.ancestry + "-Given_Name.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_half_elf_given_name(self):
        # LOCAL VARIABLES
        randoChance = rand_percent()

        # Human, Elf, or Half-Elf given name
        if randoChance <= 33:
            # Human
            self.ancestry = "Human"
            # Determine ethnicity
            humanEthnicity = self._get_human_ethnicity()
            if humanEthnicity is "Nidalese":
                humanEthnicity = "Taldan"
            self.ethnicity = humanEthnicity
            # Determine subgroup
            tempSubgroup = self._get_human_subgroup()
            self.subgroup = tempSubgroup
            # Generate given name
            self._rando_given_name()
            # Add notes
            self._add_note("Given name is %s in origin" % humanEthnicity)
            if tempSubgroup:
                self._add_note("Non-Elven ancestor is from the %s subgroup" % tempSubgroup)
        elif randoChance <= 66:
            # Half-Elf
            if self.gender is self.genderList[0]:
                self._rando_male_given_name()
            else:
                self._rando_female_given_name()
            self._add_note("Half-Elf given name")
        else:
            # Elf
            # NOTE: This may be bad but I guarantee it's easy
            self.ancestry = "Elf"
            self._rando_given_name()
            self._add_note("Given name is Elven in origin")

        # RESET ATTRIBUTES
        self.ancestry = "Half-Elf"
        self.ethnicity = None
        self.subgroup = None


    def _rando_male_given_name(self):
        self.givenName = self._get_male_given_name()


    def _get_male_given_name(self):       
        if self.ancestry is "Human":
            if self.subgroup:
                if self.subgroup is "Mauxi":
                    dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Bonuwat-Given_Name-Male.txt"
                else:
                    dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-" + self.subgroup + "-Given_Name-Male.txt"
            else:
                dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name-Male.txt"
        else:
            dbName = "Names-" + self.ancestry + "-Given_Name-Male.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_female_given_name(self):
        self.givenName = self._get_female_given_name()


    def _get_female_given_name(self):
        if self.ancestry is "Human":
            if self.subgroup:
                if self.subgroup is "Mauxi":
                    dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Bonuwat-Given_Name-Female.txt"
                else:
                    dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-" + self.subgroup + "-Given_Name-Female.txt"
            else:
                dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name-Female.txt"
        else:
            dbName = "Names-" + self.ancestry + "-Given_Name-Female.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_surname(self):
        if self.ancestry is "Elf":
            self._rando_elf_surname()
        elif self.ancestry is "Dwarf":
            self._rando_dwarf_surname()
        elif self.ancestry is "Gnome" or self.ancestry is "Goblin":
            self.surname = ""
        elif self.ancestry is "Human":
            self.surname = self._get_human_surname()
        elif self.ancestry == "Half-Elf":
            self.surname = self._get_half_elf_surname()
        else:
            self.surname = self._get_default_surname()


    def _get_half_elf_surname(self):
        # LOCAL VARIABLES
        randoChance = rand_percent()
        halfElfSurname = ""

        # GET SURNAME
        if randoChance <= 33:
            # Human
            self.ancestry = "Human"
            if not self.ethnicity:
                self.ethnicity = self._get_human_ethnicity()
            self.subgroup = self._get_human_subgroup()
            halfElfSurname = self._get_human_surname()
            self._add_note("Surname is Human (%s) in origin" % self.ethnicity)
            if self.subgroup:
                self._add_note("Surname comes from the %s subgroup" % self.subgroup)
        elif randoChance <= 66:
            # Blank
            halfElfSurname = ""
            self._add_note("Character has forgotten, hidden, denied, or does not know their surname")
        else:
            # Elf
            self.ancestry = "Elf"
            halfElfSurname = self._get_elf_surname()
            self._add_note("Surname is of Elven orgin")

        # RESET ATTRIBUTES
        self.ancestry = "Half-Elf"
        self.ethnicity = None
        self.subgroup = None

        return halfElfSurname


    def _get_human_surname(self):
        if self.ethnicity is "Garundi":
            retSurname = "from %s" % self._rando_human_surname()
        elif self.ethnicity is "Keleshite":
            retSurname = "al-%s %s %s al-%s" % (self._rando_human_surname(),
                                                self._rando_human_surname(),
                                                self._rando_human_surname(),
                                                self._rando_human_surname())
        elif self.ethnicity is "Kellid":
            retSurname = ""
        elif self.ethnicity is "Mwangi":
            retSurname = "from the %s" % self._get_subgroup_surname()
        elif self.ethnicity is "Shoanti":
            retSurname = "%s of the %s" % (self._rando_human_surname(),
                                           self._get_shoanti_clan())
        elif self.ethnicity is "Tian":
            retSurname = self._get_subgroup_surname()
        else:
            retSurname = self._rando_human_surname()

        return retSurname


    def _rando_elf_surname(self):
        self.surname = self._get_elf_surname()


    def _get_elf_surname(self):
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

        return elvenSurname % (relationship, father)


    def _rando_dwarf_surname(self):
        dwarfSurname = "of %s"
        dwarfClan = self._get_default_surname()
        self.surname = dwarfSurname % (dwarfClan)


    def _get_default_surname(self):
        dbName = "Names-" + self.ancestry + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _get_subgroup_surname(self):
        if self.subgroup is "Mauxi":
            dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Bonuwat-Surname.txt"
        else:
            dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-" + self.subgroup + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_human_ethnicity(self):
        """Initialize the ethnicity attribute"""
        self.ethnicity = self._get_human_ethnicity()


    def _rando_mwangi_subgroup(self):
        """Initialize the subgroup attribute"""
        self.subgroup = self._get_mwangi_subgroup()


    def _get_mwangi_subgroup(self):
        return random.choice(self.mwangiSubgroups)


    def _get_human_ethnicity(self):
        """Randomly select a Human ethnicity"""
        humanEthnicity = "Nidalese"

        while humanEthnicity == "Nidalese":
            humanEthnicity = random.choice(self.humanEthnicities)

        return humanEthnicity


    def _get_shoanti_clan(self):
        """Return a Shoanti clan"""
        return random.choice(self.shoantiClans)


    def _rando_human_surname(self):
        """Return a Human surname based on ethnicity"""
        dbName = "Names-" + self.ancestry + "-" + self.ethnicity + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", dbName))


    def _rando_human_subgroup(self):
        """Initialize the subgroup attribute for a Human ethnicity, if applicable"""
        self.subgroup = self._get_human_subgroup()


    def _get_human_subgroup(self):
        """Randomize a subgroup for a Human ethnicity, if applicable"""
        # LOCAL VARIABLE
        newSubgroup = None

        # RANDOMIZE
        if self.ethnicity == "Mwangi":
            newSubgroup = self._get_mwangi_subgroup()
        elif self.ethnicity is "Tian":
            newSubgroup = "Shu"  # See: User Story 7 for additional subgroups)

        return newSubgroup


    def _add_note(self, oneNote):
        """Adds one note to the notes attribute"""
        if isinstance (self.notes, list):
            self.notes.append(oneNote)
        elif isinstance (self.notes, str):
            self.notes = [self.notes] + [oneNote]
        else:
            self.notes = oneNote
