"""Defines the GGAncestry class."""

# Standard
import os
import random
# Third Party
# Local
from gamemaster_guidance.gg_file_io import pick_entry
from gamemaster_guidance.gg_globals import ANCESTRY_LIST, HUMAN_ETHNICITY_LIST
from gamemaster_guidance.gg_rando import rand_percent


# pylint: disable=too-many-instance-attributes
class GGAncestry:
    """Generates Pathfinder 2e character ancestry data."""
    humanEthnicities = HUMAN_ETHNICITY_LIST
    mwangiSubgroups = ["Bekyar", "Bonuwat", "Mauxi", "Zenj"]
    shoantiClans = ["Lyrune-Quah (Moon Clan)", "Shadde-Quah (Axe Clan)",
                    "Shriikirri-Quah (Hawk Clan)",
                    "Shundar-Quah (Spire Clan)", "Sklar-Quah (Sun Clan)",
                    "Skoan-Quah (Skull Clan)", "Tamiir-Quah (Wind Clan)"]
    supportedAncestry = ANCESTRY_LIST
    genderList = ["Male", "Female"]

    def __init__(self, race=None, sex=None, city_object=None):
        """Class constructor"""
        self.ethnicity = None
        self.subgroup = None
        self.notes = None
        self.city_obj = city_object
        self.given_name = ''  # Character's first name
        self.surname = ''  # Character's last name
        self.full_name = ''  # Character's full name

        # Ancestry
        if race and race not in self.supportedAncestry:
            raise RuntimeError(f"Unsupported race: {race}")
        if race:
            self.ancestry = race
        else:
            if self.city_obj:
                self._rando_city_ancestry()
            else:
                self._rando_ancestry()
        # Randomize a Human ethnicity and subgroup (if appropriate)
        if self.ancestry == "Human" and self.city_obj:
            self._rando_human_city_ethnicity()
        elif self.ancestry == "Human":
            self._rando_human_ethnicity()
        if self.ethnicity == "Nidalese":
            self.ethnicity = "Taldan"  # Fix this in User Story #8
        self._rando_human_subgroup()

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
        """Get the character's full name."""
        return self.full_name

    def return_race(self):
        """Get the character's ancestry."""
        return self.ancestry

    def return_ethnicity(self):
        """Get the character's ethnicity."""
        return self.ethnicity

    def return_subgroup(self):
        """Get the character's ethnic subgroup."""
        return self.subgroup

    def return_sex(self):
        """Get the character's gender."""
        return self.gender

    def return_notes(self):
        """Get the character notes."""
        return self.notes

    def _rando_ancestry(self):
        """Initialize the ancestry attribute"""
        self.ancestry = random.choice(self.supportedAncestry)

    def _rando_city_ancestry(self):
        """Initialize the ancestry attribute using city object"""
        self.ancestry = self.city_obj.rando_city_race()

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
        if self.subgroup == "Shu":
            self.full_name = f'{self.surname} {self.given_name}'
        else:
            self.full_name = f'{self.given_name} {self.surname}'

    def _rando_given_name(self):
        if self.ancestry in ('Gnome', 'Goblin'):
            self.given_name = self._get_default_given_name()
        elif self.ancestry == "Half-Elf":
            self._rando_half_elf_given_name()
        elif self.gender == self.genderList[0]:
            self._rando_male_given_name()
        else:
            self._rando_female_given_name()

    def _get_default_given_name(self):
        if self.ancestry == "Human":
            db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name.txt"
        else:
            db_name = "Names-" + self.ancestry + "-Given_Name.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _rando_half_elf_given_name(self):
        # LOCAL VARIABLES
        rando_chance = rand_percent()

        # Human, Elf, or Half-Elf given name
        if rando_chance <= 33:
            # Human
            self.ancestry = "Human"
            # Determine ethnicity
            human_ethnicity = self._get_human_ethnicity()
            if human_ethnicity == "Nidalese":
                human_ethnicity = "Taldan"
            self.ethnicity = human_ethnicity
            # Determine subgroup
            temp_subgroup = self._get_human_subgroup()
            self.subgroup = temp_subgroup
            # Generate given name
            self._rando_given_name()
            # Add notes
            self._add_note(f'Given name is {human_ethnicity} in origin')
            if temp_subgroup:
                self._add_note(f'Non-Elven ancestor is from the {temp_subgroup} subgroup')
        elif rando_chance <= 66:
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
        self.given_name = self._get_male_given_name()

    def _get_male_given_name(self):
        if self.ancestry == "Human":
            if self.subgroup:
                if self.subgroup == "Mauxi":
                    db_name = "Names-" + self.ancestry + "-" + self.ethnicity \
                             + "-Bonuwat-Given_Name-Male.txt"
                else:
                    db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-" \
                             + self.subgroup + "-Given_Name-Male.txt"
            else:
                db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name-Male.txt"
        else:
            db_name = "Names-" + self.ancestry + "-Given_Name-Male.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _rando_female_given_name(self):
        self.given_name = self._get_female_given_name()

    def _get_female_given_name(self):
        if self.ancestry == "Human":
            if self.subgroup:
                if self.subgroup == "Mauxi":
                    db_name = "Names-" + self.ancestry + "-" + self.ethnicity \
                             + "-Bonuwat-Given_Name-Female.txt"
                else:
                    db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-" \
                             + self.subgroup + "-Given_Name-Female.txt"
            else:
                db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-Given_Name-Female.txt"
        else:
            db_name = "Names-" + self.ancestry + "-Given_Name-Female.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _rando_surname(self):
        if self.ancestry == 'Elf':
            self._rando_elf_surname()
        elif self.ancestry == 'Dwarf':
            self._rando_dwarf_surname()
        elif self.ancestry in ('Gnome', 'Goblin', 'Half-Orc', 'Kitsune', 'Tengu', 'Wayang'):
            self.surname = ''
        elif self.ancestry == 'Human':
            self.surname = self._get_human_surname()
        elif self.ancestry == 'Half-Elf':
            self.surname = self._get_half_elf_surname()
        else:
            self.surname = self._get_default_surname()

    def _get_half_elf_surname(self):
        # LOCAL VARIABLES
        rando_chance = rand_percent()
        half_elf_surname = ""

        # GET SURNAME
        if rando_chance <= 33:
            # Human
            self.ancestry = "Human"
            if not self.ethnicity:
                self.ethnicity = self._get_human_ethnicity()
            self.subgroup = self._get_human_subgroup()
            half_elf_surname = self._get_human_surname()
            self._add_note(f'Surname is Human ({self.ethnicity}) in origin')
            if self.subgroup:
                self._add_note(f'Surname comes from the {self.subgroup} subgroup')
        elif rando_chance <= 66:
            # Blank
            half_elf_surname = ""
            self._add_note("Character has forgotten, hidden, denied, or "
                           "does not know their surname")
        else:
            # Elf
            self.ancestry = "Elf"
            half_elf_surname = self._get_elf_surname()
            self._add_note("Surname is of Elven orgin")

        # RESET ATTRIBUTES
        self.ancestry = "Half-Elf"
        self.ethnicity = None
        self.subgroup = None

        return half_elf_surname

    def _get_human_surname(self):
        if self.ethnicity == "Garundi":
            ret_surname = f'from {self._rando_human_surname()}'
        elif self.ethnicity == "Keleshite":
            ret_surname = f'al-{self._rando_human_surname()} {self._rando_human_surname()} ' \
                          f'{self._rando_human_surname()} al-{self._rando_human_surname()}'
        elif self.ethnicity == "Kellid":
            ret_surname = ''
        elif self.ethnicity == "Mwangi":
            ret_surname = f'from the {self._get_subgroup_surname()}'
        elif self.ethnicity == "Shoanti":
            ret_surname = f'{self._rando_human_surname()} of the {self._get_shoanti_clan()}'
        elif self.ethnicity == "Tian":
            ret_surname = self._get_subgroup_surname()
        else:
            ret_surname = self._rando_human_surname()

        return ret_surname

    def _rando_elf_surname(self):
        self.surname = self._get_elf_surname()

    def _get_elf_surname(self):
        elven_surname = "%s of %s"
        # Relationship
        if self.gender is self.genderList[0]:
            relationship = "son"
        else:
            relationship = "daughter"
        # Father's name
        father = self.given_name
        while father is self.given_name:
            father = self._get_male_given_name()

        return elven_surname % (relationship, father)

    def _rando_dwarf_surname(self):
        dwarf_surname = "of %s"
        dwarf_clan = self._get_default_surname()
        self.surname = dwarf_surname % (dwarf_clan)

    def _get_default_surname(self):
        db_name = "Names-" + self.ancestry + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _get_subgroup_surname(self):
        if self.subgroup == "Mauxi":
            db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-Bonuwat-Surname.txt"
        else:
            db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-" \
                     + self.subgroup + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _rando_human_ethnicity(self):
        """Initialize the ethnicity attribute"""
        self.ethnicity = self._get_human_ethnicity()

    def _rando_human_city_ethnicity(self):
        """Initialize the ethnicity attribute from the city object"""
        self.ethnicity = self.city_obj.rando_human_ethnicity()

    def _rando_mwangi_subgroup(self):
        """Initialize the subgroup attribute"""
        self.subgroup = self._get_mwangi_subgroup()

    def _get_mwangi_subgroup(self):
        return random.choice(self.mwangiSubgroups)

    def _get_human_ethnicity(self):
        """Randomly select a Human ethnicity"""
        human_ethnicity = "Nidalese"  # See: User Story 8

        while human_ethnicity == "Nidalese":
            human_ethnicity = random.choice(self.humanEthnicities)

        return human_ethnicity

    def _get_shoanti_clan(self):
        """Return a Shoanti clan"""
        return random.choice(self.shoantiClans)

    def _rando_human_surname(self):
        """Return a Human surname based on ethnicity"""
        db_name = "Names-" + self.ancestry + "-" + self.ethnicity + "-Surname.txt"
        return pick_entry(os.path.join(os.getcwd(), "databases", db_name))

    def _rando_human_subgroup(self):
        """Initialize the subgroup attribute for a Human ethnicity, if applicable"""
        self.subgroup = self._get_human_subgroup()

    def _get_human_subgroup(self):
        """Randomize a subgroup for a Human ethnicity, if applicable"""
        # LOCAL VARIABLE
        new_subgroup = None

        # RANDOMIZE
        if self.ethnicity == "Mwangi":
            new_subgroup = self._get_mwangi_subgroup()
        elif self.ethnicity == "Tian":
            new_subgroup = "Shu"  # See: User Story 7 for additional subgroups)

        return new_subgroup

    def _add_note(self, one_note):
        """Adds one note to the notes attribute"""
        if isinstance(self.notes, list):
            self.notes.append(one_note)
        elif isinstance(self.notes, str):
            self.notes = [self.notes] + [one_note]
        else:
            self.notes = one_note
