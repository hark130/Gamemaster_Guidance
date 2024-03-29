# Standard
from collections import OrderedDict
# Third Party
import inflect
import locale
import math
import random
# Local
from gamemaster_guidance.gg_globals import (ANCESTRY_LIST, CITY_MODIFIER_LIST, CITY_SIZE_LIMITS,
                                            HUMAN_ETHNICITY_LIST, print_header)
from gamemaster_guidance.gg_rando import rand_float, rand_integer
import gamemaster_guidance.gg_globals as GG_Globals  # For backwards compatibility


def get_key_value(theDict, theKey):
    """Returns the key value as a float, 0.0 on Exception"""
    try:
        theValue = float(theDict[theKey])
    except Exception:
        theValue = float(0.0)

    return theValue


class GG_City:
    supportedDisadvantages = ["Anarchy", "Cursed", "Hunted", "Impoverished", "Plagued"]
    supportedGovernments = ["Autocracy", "Council", "Magical", "Overlord", "Secret Syndicate"]
    supportedQualities = ["Academic", "Holy Site", "Insular", "Magically Attuned", "Notorious",
                          "Pious", "Prosperous", "Racially Intolerant", "Rumormongering Citizens",
                          "Strategic Location", "Superstitious", "Tourist Attraction"]
    supportedEthics = ["Lawful", "Neutral", "Chaotic"]
    supportedMoralities = ["Good", "Neutral", "Evil"]
    settlementStatistics = {
        "Thorp": {"Modifiers": -4, "Qualities": 1, "Danger": -10, "Base Value": 50,
                  "Purchase Limit": 500, "Spellcasting": 1, "Base Value": 50},
        "Hamlet": {"Modifiers": -2, "Qualities": 1, "Danger": -5, "Base Value": 200,
                   "Purchase Limit": 1000, "Spellcasting": 2, "Base Value": 200},
        "Village": {"Modifiers": -1, "Qualities": 2, "Danger": 0, "Base Value": 500,
                    "Purchase Limit": 2500, "Spellcasting": 3, "Base Value": 500},
        "Small Town": {"Modifiers": 0, "Qualities": 2,  "Danger": 0, "Base Value": 1000,
                       "Purchase Limit": 5000, "Spellcasting": 4, "Base Value": 1000},
        "Large Town": {"Modifiers": 0, "Qualities": 3, "Danger": 5, "Base Value": 2000,
                       "Purchase Limit": 10000, "Spellcasting": 5, "Base Value": 2000},
        "Small City": {"Modifiers": 1, "Qualities": 4, "Danger": 5, "Base Value": 4000,
                       "Purchase Limit": 25000, "Spellcasting": 6, "Base Value": 4000},
        "Large City": {"Modifiers": 2, "Qualities": 5, "Danger": 10, "Base Value": 8000,
                       "Purchase Limit": 50000, "Spellcasting": 7, "Base Value": 8000},
        "Metropolis": {"Modifiers": 4, "Qualities": 6, "Danger": 10, "Base Value": 16000,
                       "Purchase Limit": 100000, "Spellcasting": 8, "Base Value": 16000}
    }

    def __init__(self, cityDict):
        """Class constructor"""
        self.cityDict = cityDict
        self.baseCityModifier = None
        self.npcMultiplier = 1  # Large cities can have multiple high-level NPCs
        self.npcClassLevels = {}  # class:totals for population
        self.race_lookup = {}  # race:percentage dictionary defined by _parse_city()
        self.population = 0  # Store total population here

        # Use these attributes to indicate a value should be randomized prior to parsing
        self.randoDisadvantage = False  # Randomize a disadvantage
        self.randoAlignment = False
        self.randoGovernment = False
        self.randoPopulation = False
        self.randoQualities = False

        # Use these attributes to indicate a value should be calculated prior to parsing
        self.calcBaseValue = False
        self.calcMagicItems = False
        self.calcNPCs = False
        self.calcType = False

    def load(self):
        """Entry level method: validate and parse the dictionary"""
        self._validate_city()  # Verify all input
        self._complete_city()  # Fill in the blanks
        # Everything prior to this method call should operate on the cityDict
        self._parse_city()     # Load the city into attributes

    def get_race_percent(self, raceName):
        """Return a race's percent"""
        return self.race_lookup[raceName]

    def rando_city_race(self):
        # LOCAL VARIABLES
        totalPercent = float(0.0)

        # DETERMINE RACE
        # Add total percents
        for percentValue in self.race_lookup.values():
            totalPercent += percentValue
        if totalPercent <= 0.0:
            raise RuntimeError("Race percentages not found")
        # Rando a number
        randoPercent = rand_float(0.0, totalPercent)
        # Find the match
        totalPercent = 0.0
        for race, percent in self.race_lookup.items():
            totalPercent += percent
            if randoPercent <= totalPercent:
                if race in HUMAN_ETHNICITY_LIST:
                    return GG_Globals.GG_CITY_RACE_HUMAN
                else:
                    return race

        # DONE
        raise RuntimeError("Race not found")

    def rando_human_ethnicity(self):
        # LOCAL VARIABLES
        totalPercent = float(0.0)  # Running total of percentages

        # DETERMINE ETHNICITY
        # Add total percents
        totalPercent = self._total_human_ethnic_percentages()
        # Rando a number
        randoPercent = rand_float(0.0, totalPercent)
        # Find the match
        totalPercent = 0.0
        for humanEthnicity in HUMAN_ETHNICITY_LIST:
            totalPercent += self.race_lookup[humanEthnicity]
            if randoPercent <= totalPercent:
                return humanEthnicity

        # DONE
        raise RuntimeError("Human ethnicity not found")

    def print_city_details(self):
        # GENERAL
        self._print_city_general_details()

        # DEMOGRAPHICS
        self._print_city_demographic_details()

        # MARKETPLACE
        self._print_city_marketplace_details()

    def print_city_npcs(self):
        if self.npcs:
            print("NPCs")
            for npc in self.npcs:
                print("    {}".format(npc))

    def rando_npc_class_level(self, minLevel=1):
        """Randomize a class and level based on city statistics.

        Randomize a class and level based on city statistics: tuple(("class": str, level: int)).
        """
        # LOCAL VARIABLES
        retRando = None  # tuple(("class", level))

        # FIND A CITIZEN
        # 1. Find valid NPC class dictionaries
        npcClassLevelList = self._find_valid_npc_dicts(minLevel)

        # 2. Count the available population
        if npcClassLevelList:
            validPopCount = self._count_valid_npcs(npcClassLevelList, minLevel=minLevel)
        else:
            raise RuntimeError(f"Unable to find a citizen of minimum level {minLevel}")

        # 3. Randomize a citizen number
        if validPopCount > 0:
            randoCitizen = rand_integer(1, validPopCount)  # Random citizen
        else:
            raise RuntimeError(f"Unable to find a citizen of minimum level {minLevel}")

        # 4. Find that citizen
        if randoCitizen > 0:
            retRando = self._find_a_citizen(npcClassLevelList, randoCitizen, minLevel=minLevel)
        else:
            raise RuntimeError(f"Unable to find a citizen of minimum level {minLevel}")

        # DONE
        return retRando

    def _find_valid_npc_dicts(self, minLevel=1):
        """Returns a list of npcClassLevels dicts that contain at least one match for minLevel"""
        # LOCAL VARIABLES
        retList = []

        # SEARCH DICTIONARIES
        for (nclKey, nclValue) in self.npcClassLevels.items():
            # Skip it if it's empty
            if nclValue["Total"] > 0:
                for (nclvKey, nclvValue) in nclValue["Dict"].items():
                    if nclvKey >= minLevel and nclvValue > 0:
                        retList.append({nclKey: nclValue})
                        break

        # DONE
        return retList

    def _count_valid_npcs(self, classDictList, minLevel=1):
        # LOCAL VARIABLES
        retCount = 0

        # VALIDATION
        # If minimum level is 1, return the sum of all the totals
        if minLevel == 1:
            for classDict in classDictList:
                for value in classDict.values():
                    retCount += value["Total"]
        else:
            for classDict in classDictList:
                for value in classDict.values():
                    for (level, number) in value["Dict"].items():
                        if level >= minLevel and number > 0:
                            retCount += number

        # DONE
        return retCount

    def _find_a_citizen(self, classDictList, citizenNum, minLevel=1):
        # LOCAL VARIABLES
        localClass = None  # Random citizen's class
        localLevel = None  # Random citizen's level
        localCitNum = citizenNum  # Local copy of citizenNum to decrement

        # FIND THE CITIZEN
        for classDict in classDictList:
            for value in classDict.values():
                for (level, number) in value["Dict"].items():
                    if level >= minLevel and number > 0:
                        if localCitNum <= number:
                            localClass = list(classDict.keys())[0]  # Class name is the only key
                            localLevel = level
                            return tuple((localClass, localLevel))
                        else:
                            localCitNum -= number

        raise RuntimeError(f'Unable to find citizen number {citizenNum} of '
                           f'minimum level {minLevel}')

    def _validate_city(self):
        """Validate the contents of cityDict"""
        self._validate_mandatory()
        self._validate_optional()
        self._validate_defined()

    def _validate_mandatory(self):
        """Validate the mandatory entries in cityDict"""
        # LOCAL VARIABLES
        mandEntries = ["name", "region", "ancestry"]

        # Top Level
        temp = self.cityDict["city"]
        # Second Level
        for mandEntry in mandEntries:
            temp = self.cityDict["city"][mandEntry]
        # Ethnicity Entries
        self._validate_ancestries()

    def _validate_ancestries(self):
        """Verifies all the ancestry entries in the city dict are in the ANCESTRY_LIST."""
        for ancestry in self.cityDict["city"]["ancestry"].keys():
            if ancestry not in ANCESTRY_LIST:
                raise RuntimeError(f'Unsupported ancestry: {ancestry}')

        self._validate_human_ethnicities()

    def _validate_human_ethnicities(self):
        for ethnicity in HUMAN_ETHNICITY_LIST:
            temp = self.cityDict["city"]["ancestry"]["Human"][ethnicity]

    def _validate_optional(self):
        """Validate any optional entries in cityDict"""
        # Disadvantages
        self._validate_disadvantages()
        # Aignment
        self._validate_alignment()
        # Government
        self._validate_government()
        # Population
        self._validate_population()
        # Qualities
        self._validate_qualities()

    def _validate_disadvantages(self):
        """Validate the disadvantages key"""
        # LOCAL VARIABLES
        disadValue = None
        disadList = []

        # GET VALUE
        try:
            disad = self.cityDict["city"]["disadvantages"]
        except KeyError:
            pass
        else:
            if isinstance(disad, str):
                disadList = [disad]
            elif isinstance(disad, list):
                disadList = disad
            elif not disad:
                disadList = []
                self.randoDisadvantage = True  # Randomize one before parsing
            else:
                disadList = [str(disad)]

        for entry in disadList:
            if entry not in self.supportedDisadvantages:
                raise RuntimeError("Unsupported disadvantage")

    def _validate_alignment(self):
        # LOCAL VARIABLES
        ethics = self.supportedEthics
        moralities = self.supportedMoralities
        good = False

        try:
            alignment = self.cityDict["city"]["alignment"]
        except KeyError:
            good = True
            self.randoAlignment = True
        else:
            for ethic in ethics:
                for moral in moralities:
                    if alignment == ethic + " " + moral:
                        good = True
                    elif alignment == ethic and ethic == moral:
                        good = True
                    if good:
                        break
                if good:
                    break

        if not good:
            raise RuntimeError("Invalid alignment")

    def _validate_government(self):
        try:
            government = self.cityDict["city"]["government"]
        except KeyError:
            self.randoGovernment = True
        else:
            if government not in self.supportedGovernments:
                raise RuntimeError("Unsupported government")

    def _validate_population(self):
        try:
            population = self.cityDict["city"]["population"]
        except KeyError:
            self.randoPopulation = True
        else:
            if not isinstance(population, int):
                try:
                    temp = locale.atoi(population)
                except Exception as err:
                    print("Invalid population: {}".format(population))
                    print(repr(err))
                    raise err

    def _validate_qualities(self):
        try:
            qualities = self.cityDict["city"]["qualities"]
        except KeyError:
            self.randoQualities = True
        else:
            if not qualities:
                self.randoQualities = True
            else:
                # Respond to type
                if isinstance(qualities, str):
                    qualities = [qualities]
                elif not isinstance(qualities, list):
                    raise TypeError("Unknown qualities entry")
                # Parse entries
                for quality in qualities:
                    if quality not in self.supportedQualities \
                      and not quality.startswith("Racially Intolerant"):
                        raise RuntimeError("Unsupported quality")

    def _validate_defined(self):
        """Validate any script-defined entries in cityDict"""
        # See: User Story 9 for full implementation
        # Base Value
        self._validate_city_base_value()
        # Magic Items

        # Modifiers
        # NOTE: REcalculate all modifiers regardless of what's in the config file

        # NPCs
        self._validate_city_npcs()

        # Purchase Limit
        # NOTE: REcalculate all purchase limits regardless of what's in the config file

        # Spellcasting

        # Type
        self._validate_city_type()

    def _validate_city_base_value(self):
        # Get it
        try:
            baseValue = self.cityDict["city"]["base_value"]
        except KeyError:
            self.calcBaseValue = True
        else:
            try:
                temp = locale.atoi(baseValue)
            except Exception as err:
                print("Invalid base value: {}".format(baseValue))
                print(repr(err))
                raise err

    def _validate_city_npcs(self):
        # Get it
        try:
            cityNPCs = self.cityDict["city"]["npcs"]
        except KeyError:
            self.calcNPCs = True
        else:
            if not cityNPCs:
                self.calcNPCs = True

    def _validate_city_type(self):
        # Get it
        try:
            localType = self.cityDict["city"]["type"]
        except KeyError:
            self.calcType = True
        else:
            if localType not in self.settlementStatistics.keys():
                raise RuntimeError("Invalid city type")

    def _complete_city(self):
        self._rando_city()  # Must come first unless population is already defined
        self._calculate_city()

    def _rando_city(self):
        """Randomize elements of a city not included in the config"""
        if self.randoPopulation:
            self._rando_population()
            self.randoPopulation = False

        if self.randoDisadvantage:
            self._rando_disadvantage()
            self.randoDisadvantage = False

        if self.randoAlignment:
            self._rando_alignment()
            self.randoAlignment = False

        if self.randoGovernment:
            self._rando_government()
            self.randoGovernment = False

    def _rando_population(self):
        """Randomizes a population into self.cityDict"""
        self.cityDict["city"]["population"] = str(rand_integer(CITY_SIZE_LIMITS[0],
                                                               CITY_SIZE_LIMITS[1]))

    def _rando_disadvantage(self):
        """Randomize one disadvantage into self.cityDict"""
        self.cityDict["city"]["disadvantages"] = [random.choice(self.supportedDisadvantages)]

    def _rando_alignment(self):
        """Randomize one alignment into self.cityDict"""
        # Rando
        localAlignment = random.choice(self.supportedEthics) + " " \
            + random.choice(self.supportedMoralities)
        # Update True Neutral
        if localAlignment == "Neutral Neutral":
            localAlignment = "Neutral"
        # Store It
        self.cityDict["city"]["alignment"] = localAlignment

    def _rando_government(self):
        """Randomize a government into self.cityDict"""
        self.cityDict["city"]["government"] = random.choice(self.supportedGovernments)

    def _calculate_city(self):
        """Calculate all the details of a city not already calculated in the config"""
        # Calculate this first since the settlement statistics are derived from it
        if self.calcType:
            self._calc_city_type()
            self.calcType = False

        # Moved from _rando_city since the "type" should be defined before the qualities
        if self.randoQualities:
            self._rando_city_qualities()
            self.randoQualities = False

        if self.calcBaseValue:
            self._calc_city_base_value()
            self.calcBaseValue = False

        if self.calcMagicItems:
            # TO DO: DON'T DO NOW
            # IDEAS:
            # 1. Put it into self.settlementStatistics
            # 2. Hard code some responses into a method
            self.calcMagicItems = False

        # Always calculate modifiers
        self._calc_city_modifiers()

        # Always calculate purchase limit
        self._calc_city_purchase_limit()

        # Always calculate spellcasting
        self._calc_city_spellcasting()

        # Magic Items
        # TO DO: DON'T DO NOW

        # NPCs
        # Moved randomization validation downwards
        # Some 'consumers' of the GG_City class need some randomized totals regardless of what's
        # already been calculated
        self._rando_city_npcs()
        self.calcNPCs = False

    def _calc_city_type(self):
        """Calculate and store the city type into cityDict"""
        # Get Population
        population = self.cityDict["city"]["population"]
        if not isinstance(population, int):
            population = locale.atoi(population)

        # Translate Population to Type
        if population <= 20:
            localType = "Thorp"
        elif population <= 60:
            localType = "Hamlet"
        elif population <= 200:
            localType = "Village"
        elif population <= 2000:
            localType = "Small Town"
        elif population <= 5000:
            localType = "Large Town"
        elif population <= 10000:
            localType = "Small City"
        elif population <= 25000:
            localType = "Large City"
        else:
            localType = "Metropolis"

        # Verify Type
        assert (localType in self.settlementStatistics.keys()), "Invalid city type"

        # Done
        self.cityDict["city"]["type"] = localType

    def _rando_city_qualities(self):
        # LOCAL VARIABLES
        localQualList = []
        tempQual = None
        numQuals = self.settlementStatistics[self.cityDict["city"]["type"]]["Qualities"]

        # INPUT VALIDATION
        assert (numQuals > 0), "Invalid number of qualities"
        assert (numQuals <= len(self.supportedQualities)), "Not enough supported qualities"

        # RANDO QUALITIES
        while len(localQualList) < numQuals:
            tempQual = random.choice(self.supportedQualities)
            if tempQual not in localQualList:
                localQualList.append(tempQual)

        # DONE
        self.cityDict["city"]["qualities"] = localQualList

    def _calc_city_base_value(self):
        """Calculate and store the city's base value.

        Calculate city's base value, adjust for qualities/disadvantages, then store it in city dict.
        """
        # LOCAL VARIABLES
        localBaseValue = self.settlementStatistics[self.cityDict["city"]["type"]]["Base Value"]
        adjustPercent = 100

        # CALCULATE ADJUSTMENTS
        # Qualities
        if "Magically Attuned" in self.cityDict["city"]["qualities"]:
            adjustPercent += 20
        if "Notorious" in self.cityDict["city"]["qualities"]:
            adjustPercent += 30
        if "Prosperous" in self.cityDict["city"]["qualities"]:
            adjustPercent += 30
        if "Strategic Location" in self.cityDict["city"]["qualities"]:
            adjustPercent += 10
        if "Tourist Attraction" in self.cityDict["city"]["qualities"]:
            adjustPercent += 20

        # Disadvantages
        try:
            if "Hunted" in self.cityDict["city"]["disadvantages"]:
                adjustPercent -= 20
            if "Impoverished" in self.cityDict["city"]["disadvantages"]:
                adjustPercent -= 50
            if "Plagued" in self.cityDict["city"]["disadvantages"]:
                adjustPercent -= 20
        except KeyError:
            pass  # Disadvantages are not mandatory

        # ADJUST BASE VALUE
        localBaseValue = localBaseValue * adjustPercent * .01

        # DONE
        self.cityDict["city"]["base_value"] = str(int(localBaseValue))

    def _calc_city_modifiers(self):
        """Calculate all six city modifiers into cityDict"""
        #   modifiers:
        self.baseCityModifier = \
            self.settlementStatistics[self.cityDict["city"]["type"]]["Modifiers"]
        self.cityDict["city"]["modifiers"] = {}  # Reset
        #     corruption:
        self._calc_city_modifier_corruption()
        #     crime:
        self._calc_city_modifier_crime()
        #     economy:
        self._calc_city_modifier_economy()
        #     law:
        self._calc_city_modifier_law()
        #     lore:
        self._calc_city_modifier_lore()
        #     society:
        self._calc_city_modifier_society()

    def _calc_city_purchase_limit(self):
        """Calculate and store the city's purchase limit.

        Calculate city's purchase limit, adjust for qualities/disadvantages, then store it in
        city dict.
        """
        # LOCAL VARIABLES
        localPurchaseLimit = \
            self.settlementStatistics[self.cityDict["city"]["type"]]["Purchase Limit"]
        adjustPercent = 100

        # CALCULATE ADJUSTMENTS
        # Qualities
        if "Magically Attuned" in self.cityDict["city"]["qualities"]:
            adjustPercent += 20
        if "Notorious" in self.cityDict["city"]["qualities"]:
            adjustPercent += 50
        if "Prosperous" in self.cityDict["city"]["qualities"]:
            adjustPercent += 50

        # Disadvantages
        try:
            if "Impoverished" in self.cityDict["city"]["disadvantages"]:
                adjustPercent -= 50
        except KeyError:
            pass  # Disadvantages are not mandatory

        # ADJUST BASE LIMIT
        localPurchaseLimit = localPurchaseLimit * adjustPercent * .01

        # DONE
        self.cityDict["city"]["purchase_limit"] = str(int(localPurchaseLimit))

    def _calc_city_spellcasting(self):
        """Calculate and store city's spellcasting.

        Calculate the city's spellcasting, adjust for qualities/disadvantages, then store it in
        city dict.
        """
        # LOCAL VARIABLES
        localSpellcasting = self.settlementStatistics[self.cityDict["city"]["type"]]["Spellcasting"]

        # CALCULATE ADJUSTMENTS
        # Government
        if self.cityDict["city"]["government"] == "Magical":
            localSpellcasting += 1

        # Qualities
        if "Academic" in self.cityDict["city"]["qualities"]:
            localSpellcasting += 1
        if "Holy Site" in self.cityDict["city"]["qualities"]:
            localSpellcasting += 2
        if "Magically Attuned" in self.cityDict["city"]["qualities"]:
            localSpellcasting += 2
        if "Pious" in self.cityDict["city"]["qualities"]:
            localSpellcasting += 1
        if "Superstitious" in self.cityDict["city"]["qualities"]:
            localSpellcasting -= 2

        # Max Spell Level
        if localSpellcasting > 10:
            localSpellcasting = 10

        # DONE
        self.cityDict["city"]["spellcasting"] = str(localSpellcasting)

    def _rando_city_npcs(self):
        """Randomize NPCs and add them to cityDict as a list"""
        if self.calcNPCs:
            # PREPARE LIST
            self.cityDict["city"]["npcs"] = []
        # UPDATE MULTIPLIER
        self._update_city_npc_multiplier()

        # CALCUALTE NPCs
        # Adept 1d6 + community modifier (Task 5-6)
        # Alchemist 1d4 + community modifier (Class)
        self._rando_city_npc_alchemists()
        # Aristocrat 1d4 + community modifier (Task 5-6)
        # Barbarian* 1d4 + community modifier (Class)
        self._rando_city_npc_barbarians()
        # Bard 1d6 + community modifier (Class)
        self._rando_city_npc_bards()
        # Champion (Paladin) 1d3 + community modifier (Class)
        self._rando_city_npc_champions()
        # Cleric 1d6 + community modifier (Class)
        self._rando_city_npc_clerics()
        # Commoner 4d4 + community modifier (Task 5-6)
        # Druid 1d6 + community modifier (Class)
        self._rando_city_npc_druids()
        # Expert 3d4 + community modifier (Task 5-6)
        # Fighter 1d8 + community modifier (Class)
        self._rando_city_npc_fighters()
        # Monk* 1d4 + community modifier (Class)
        self._rando_city_npc_monks()
        # Ranger 1d3 + community modifier (Class)
        self._rando_city_npc_rangers()
        # Rogue 1d8 + community modifier (Class)
        self._rando_city_npc_rogues()
        # Sorcerer 1d4 + community modifier (Class)
        self._rando_city_npc_sorcerers()
        # Warrior 2d4 + community modifier (Task 5-6)
        # Wizard 1d4 + community modifier (Class)
        self._rando_city_npc_wizards()

        # Remaining Population
        # Take the remaining population after all other characters are generated
        # and divide it up so that 91% are commoners, 5% are warriors, 3%
        # are experts, and the remaining 1% is equally divided between
        # aristocrats and adepts (0.5% each)
        self._rando_remaining_npc_population()

        # Add Notes
        # TO DO: DON'T DO NOW
        # Randomize who the town guard is

    def _rando_remaining_npc_population(self):
        # LOCAL VARIABLES
        currentRemainingPop = int(self.cityDict["city"]["population"])
        remainderDict = {"aristocrat": 0, "adept": 0, "expert": 0, "warrior": 0, "commoner": 0}

        # 1. Determine remaining population
        for valueDict in self.npcClassLevels.values():
            currentRemainingPop -= valueDict["Total"]
        # Account for underflow population
        if currentRemainingPop > 0:
            # 2. Calcualate remaining totals
            remainderDict["aristocrat"] = int(currentRemainingPop * .005)
            remainderDict["adept"] = int(currentRemainingPop * .005)
            remainderDict["expert"] = int(currentRemainingPop * .03)
            remainderDict["warrior"] = int(currentRemainingPop * .05)
            remainderDict["commoner"] = (currentRemainingPop
                                         - remainderDict["aristocrat"] - remainderDict["adept"]
                                         - remainderDict["expert"] - remainderDict["warrior"])
            assert ((remainderDict["aristocrat"] + remainderDict["adept"]
                     + remainderDict["expert"] + remainderDict["warrior"]
                     + remainderDict["commoner"]) == currentRemainingPop), \
                   "Remaining population miscalculation"
        else:
            for key in remainderDict.keys():
                remainderDict[key] = 0

        # 3. Update NPC class levels
        for (key, value) in remainderDict.items():
            if value > 0:
                self._set_npc_class(key, 1, value)

    def _update_city_npc_multiplier(self):
        # LOCAL VARIABLES
        cityType = self.cityDict["city"]["type"]

        # UPDATE MULTIPLIER
        if cityType == "Metropolis":
            self.npcMultiplier = 4
        elif cityType == "Large City":
            self.npcMultiplier = 3
        elif cityType == "Small City":
            self.npcMultiplier = 2
        elif cityType:
            self.npcMultiplier = 1
        else:
            raise RuntimeError("Invalid city type found in cityDict")

    def _rando_city_npc_alchemists(self):
        # LOCAL VARIABLES
        upperLimit = 4  # Alchemist 1d4

        # CALCULATE TOTAL
        self._rando_npc_class("alchemist", 1, upperLimit)

    def _rando_city_npc_barbarians(self):
        # LOCAL VARIABLES
        upperLimit = 4  # Barbarian* 1d4

        # CALCULATE TOTAL
        # Adjust limit
        if self._are_barbarians_common():
            upperLimit = 8
        # Rando levels
        self._rando_npc_class("barbarian", 1, upperLimit)

    def _are_barbarians_common(self):
        return self._determine_human_barbarian_average() >= self._determine_human_ethnic_average()

    def _total_human_ethnic_percentages(self):
        """Return the total of all human ethnic percentages"""
        # LOCAL VARIABLES
        runningPercentTotal = 0.0

        # GET TOTAL
        for humanEthnicity in HUMAN_ETHNICITY_LIST:
            runningPercentTotal += self.cityDict["city"]["ancestry"]["Human"][humanEthnicity]

        # DONE
        return runningPercentTotal

    def _determine_human_ethnic_average(self):
        """Return the average of all human ethnic percentages"""
        # LOCAL VARIABLES
        runningPercentTotal = 0.0
        ethnicTotal = 0
        retAverage = 0.0

        # GET AVERAGE
        # Total
        runningPercentTotal = self._total_human_ethnic_percentages()
        ethnicTotal = len(HUMAN_ETHNICITY_LIST)
        # Average
        retAverage = runningPercentTotal / ethnicTotal

        return retAverage

    def _determine_human_barbarian_average(self):
        """Return the total percent of Kellid and Ulfen ethnic percentages"""
        # LOCAL VARIABLES
        runningPercentTotal = 0.0
        retAverage = 0.0

        # GET AVERAGE
        # Total
        runningPercentTotal += \
            self.cityDict["city"]["ancestry"]["Human"][GG_Globals.GG_CITY_RACE_KELLID]
        runningPercentTotal += \
            self.cityDict["city"]["ancestry"]["Human"][GG_Globals.GG_CITY_RACE_ULFEN]
        # Average
        retAverage = runningPercentTotal / 2

        return retAverage

    def _rando_city_npc_bards(self):
        # LOCAL VARIABLES
        upperLimit = 6  # Bard 1d6

        # CALCULATE TOTAL
        self._rando_npc_class("bard", 1, upperLimit)

    def _rando_city_npc_champions(self):
        # LOCAL VARIABLES
        upperLimit = 3  # Champion (Paladin) 1d3

        # CALCULATE TOTAL
        self._rando_npc_class("champion", 1, upperLimit)

    def _rando_city_npc_clerics(self):
        # LOCAL VARIABLES
        upperLimit = 6  # Cleric 1d6

        # CALCULATE TOTAL
        self._rando_npc_class("cleric", 1, upperLimit)

    def _rando_city_npc_druids(self):
        # LOCAL VARIABLES
        upperLimit = 6  # Druid 1d6

        # CALCULATE TOTAL
        self._rando_npc_class("druid", 1, upperLimit)

    def _rando_city_npc_fighters(self):
        # LOCAL VARIABLES
        upperLimit = 8  # Fighter 1d8

        # CALCULATE TOTAL
        self._rando_npc_class("fighter", 1, upperLimit)

    def _rando_city_npc_monks(self):
        # LOCAL VARIABLES
        upperLimit = 4  # Monk* 1d4

        # CALCULATE TOTAL
        # Adjust limit
        if self._are_monks_common():
            upperLimit = 8
        # Rando levels
        self._rando_npc_class("monk", 1, upperLimit)

    def _are_monks_common(self):
        """Determine if monk-centric races/ethnicities/subgroups are common"""
        return self._determine_human_monk_average() >= self._determine_human_ethnic_average()

    def _determine_human_monk_average(self):
        return self.cityDict["city"]["ancestry"]["Human"][GG_Globals.GG_CITY_RACE_TIAN]

    def _rando_city_npc_rangers(self):
        # LOCAL VARIABLES
        upperLimit = 3  # Ranger 1d3

        # CALCULATE TOTAL
        self._rando_npc_class("ranger", 1, upperLimit)

    def _rando_city_npc_rogues(self):
        # LOCAL VARIABLES
        upperLimit = 8  # Rogue 1d8

        # CALCULATE TOTAL
        self._rando_npc_class("rogue", 1, upperLimit)

    def _rando_city_npc_sorcerers(self):
        # LOCAL VARIABLES
        upperLimit = 4  # Sorcerer 1d4

        # CALCULATE TOTAL
        self._rando_npc_class("sorcerer", 1, upperLimit)

    def _rando_city_npc_wizards(self):
        # LOCAL VARIABLES
        upperLimit = 4  # Wizard 1d4

        # CALCULATE TOTAL
        self._rando_npc_class("wizard", 1, upperLimit)

    def _rando_npc_class(self, className, numDice, numFaces):
        # LOCAL VARIABLES
        levelDict = {}
        charLevel = 1  # Current level being enumerated for this class
        numOfThatLevel = 1  # Number of NPCs at level "charLevel"

        # Initialize the dictionary
        for level in range(1, 21):
            levelDict[level] = 0  # Initialize each level

        # CALCULATE LEVELS
        for _ in range(self.npcMultiplier):
            numOfThatLevel = 1  # Reset temp variable
            charLevel = self._calc_highest_level(numDice, numFaces)
            if charLevel > 0:
                levelDict[charLevel] += numOfThatLevel
                while charLevel >= 2:
                    charLevel = math.ceil(charLevel / 2)
                    numOfThatLevel *= 2
                    levelDict[charLevel] += numOfThatLevel

        # Validation of calcualting NPCs moved down to ensure this class always...
        if self.calcNPCs:
            self._translate_level_dict_into_npc_list(className, levelDict)
        # ...calculates total 'population' of each class for the sake of class-based randomization
        self._update_npc_class_totals(className, levelDict)

    def _set_npc_class(self, className, charLevel, numOfThatLevel):
        levelDict = {charLevel: numOfThatLevel}

        # Validation of calcualting NPCs moved down to ensure this class always...
        if self.calcNPCs:
            self._translate_level_dict_into_npc_list(className, levelDict)
        # ...calculates total 'population' of each class for the sake of class-based randomization
        self._update_npc_class_totals(className, levelDict)

    def _calc_highest_level(self, numDice, numFaces):
        """Return the highest NPC level given numDice-d-numFaces + self.baseCityModifier"""
        # LOCAL VARIABLES
        runningTotal = 0

        # ADD IT UP
        for _ in range(numDice):
            runningTotal += rand_integer(1, numFaces)
        runningTotal += self.baseCityModifier

        # DONE
        return runningTotal

    def _translate_level_dict_into_npc_list(self, className, levelDict):
        # LOCAL VARIABLES
        sortedDictKeys = list(levelDict.keys())
        sortedDictKeys.sort(reverse=True)
        npcListEntry = ""
        numToWord = inflect.engine()

        for level in sortedDictKeys:
            if levelDict[level] > 0:
                npcListEntry = numToWord.number_to_words(levelDict[level]).capitalize() + " " \
                               + numToWord.ordinal(level) + " level " + className
                if levelDict[level] > 1:
                    npcListEntry = npcListEntry + "s"
                self.cityDict["city"]["npcs"].append(npcListEntry)

    def _update_npc_class_totals(self, className, levelDict):
        # LOCAL VARIABLES
        classTotal = 0

        for value in levelDict.values():
            classTotal += value

        self.npcClassLevels[className] = {"Total": classTotal, "Dict": levelDict}

    def _calc_city_modifier_corruption(self):
        # LOCAL VARIABLES
        localCorruption = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].endswith("Evil"):
            localCorruption += 1

        # Government
        if self.cityDict["city"]["government"] == "Magical":
            localCorruption -= 2
        elif self.cityDict["city"]["government"] == "Overlord":
            localCorruption += 2
        elif self.cityDict["city"]["government"] == "Secret Syndicate":
            localCorruption += 2

        # Qualities
        if "Holy Site" in self.cityDict["city"]["qualities"]:
            localCorruption -= 2

        # Disadvantages
        try:
            if "Anarchy" in self.cityDict["city"]["disadvantages"]:
                localCorruption += 4
            if "Impoverished" in self.cityDict["city"]["disadvantages"]:
                localCorruption += 1
        except KeyError:
            pass  # Disadvantages are not mandatory

        # DONE
        self.cityDict["city"]["modifiers"].update({"corruption": str(localCorruption)})

    def _calc_city_modifier_crime(self):
        # LOCAL VARIABLES
        localCrime = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].startswith("Chaotic"):
            localCrime += 1

        # Government
        if self.cityDict["city"]["government"] == "Overlord":
            localCrime -= 2
        elif self.cityDict["city"]["government"] == "Secret Syndicate":
            localCrime += 2

        # Qualities
        if "Insular" in self.cityDict["city"]["qualities"]:
            localCrime -= 1
        if "Notorious" in self.cityDict["city"]["qualities"]:
            localCrime += 1
        if "Superstitious" in self.cityDict["city"]["qualities"]:
            localCrime -= 4

        # Disadvantages
        try:
            if "Anarchy" in self.cityDict["city"]["disadvantages"]:
                localCrime += 4
            if "Impoverished" in self.cityDict["city"]["disadvantages"]:
                localCrime += 1
        except KeyError:
            pass  # Disadvantages are not mandatory

        # DONE
        self.cityDict["city"]["modifiers"].update({"crime": str(localCrime)})

    def _calc_city_modifier_economy(self):
        # LOCAL VARIABLES
        localEconomy = self.baseCityModifier

        # Government
        if self.cityDict["city"]["government"] == "Secret Syndicate":
            localEconomy += 2

        # Qualities
        if "Prosperous" in self.cityDict["city"]["qualities"]:
            localEconomy += 1
        if "Strategic Location" in self.cityDict["city"]["qualities"]:
            localEconomy += 1
        if "Tourist Attraction" in self.cityDict["city"]["qualities"]:
            localEconomy += 1

        # Disadvantages
        try:
            if "Anarchy" in self.cityDict["city"]["disadvantages"]:
                localEconomy -= 4
            if "Hunted" in self.cityDict["city"]["disadvantages"]:
                localEconomy -= 4
        except KeyError:
            pass  # Disadvantages are not mandatory

        # DONE
        self.cityDict["city"]["modifiers"].update({"economy": str(localEconomy)})

    def _calc_city_modifier_law(self):
        # LOCAL VARIABLES
        localLaw = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].startswith("Lawful"):
            localLaw += 1

        # Government
        if self.cityDict["city"]["government"] == "Council":
            localLaw -= 2
        elif self.cityDict["city"]["government"] == "Overlord":
            localLaw += 2
        elif self.cityDict["city"]["government"] == "Secret Syndicate":
            localLaw -= 6

        # Qualities
        if "Insular" in self.cityDict["city"]["qualities"]:
            localLaw += 1
        if "Notorious" in self.cityDict["city"]["qualities"]:
            localLaw -= 1
        if "Superstitious" in self.cityDict["city"]["qualities"]:
            localLaw += 2

        # Disadvantages
        try:
            if "Anarchy" in self.cityDict["city"]["disadvantages"]:
                localLaw -= 6
            if "Hunted" in self.cityDict["city"]["disadvantages"]:
                localLaw -= 4
        except KeyError:
            pass  # Disadvantages are not mandatory

        # DONE
        self.cityDict["city"]["modifiers"].update({"law": str(localLaw)})

    def _calc_city_modifier_lore(self):
        # LOCAL VARIABLES
        localLore = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"] == "Neutral":
            localLore += 2
        elif self.cityDict["city"]["alignment"].endswith("Neutral"):
            localLore += 1

        # Government
        if self.cityDict["city"]["government"] == "Council":
            localLore -= 2
        elif self.cityDict["city"]["government"] == "Magical":
            localLore += 2

        # Qualities
        if "Academic" in self.cityDict["city"]["qualities"]:
            localLore += 1
        if "Rumormongering Citizens" in self.cityDict["city"]["qualities"]:
            localLore += 1

        # DONE
        self.cityDict["city"]["modifiers"].update({"lore": str(localLore)})

    def _calc_city_modifier_society(self):
        # LOCAL VARIABLES
        localSociety = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].endswith("Good"):
            localSociety += 1

        # Government
        if self.cityDict["city"]["government"] == "Council":
            localSociety += 4
        elif self.cityDict["city"]["government"] == "Magical":
            localSociety -= 2
        elif self.cityDict["city"]["government"] == "Overlord":
            localSociety -= 2

        # Qualities
        if "Rumormongering Citizens" in self.cityDict["city"]["qualities"]:
            localSociety -= 1
        if "Superstitious" in self.cityDict["city"]["qualities"]:
            localSociety += 2

        # Disadvantages
        try:
            if "Anarchy" in self.cityDict["city"]["disadvantages"]:
                localSociety -= 4
            if "Hunted" in self.cityDict["city"]["disadvantages"]:
                localSociety -= 4
        except KeyError:
            pass  # Disadvantages are not mandatory

        # DONE
        self.cityDict["city"]["modifiers"].update({"society": str(localSociety)})

    def _parse_city(self):
        """Parse the cityDict contents into attributes"""
        details_dict = self.cityDict[GG_Globals.GG_CITY_KEY]
        city_ethnicity = details_dict[GG_Globals.GG_CITY_RACE_KEY]

        self.name = details_dict[GG_Globals.GG_CITY_NAME_KEY]
        self.region = details_dict[GG_Globals.GG_CITY_REGION_KEY]
        for ancestry in ANCESTRY_LIST:
            if ancestry == GG_Globals.GG_CITY_RACE_HUMAN:
                for human_ethnicity in HUMAN_ETHNICITY_LIST:
                    try:
                        self.race_lookup[human_ethnicity] = \
                            get_key_value(city_ethnicity[GG_Globals.GG_CITY_RACE_HUMAN],
                                          human_ethnicity)
                    except KeyError:
                        self.race_lookup[human_ethnicity] = 0
            else:
                self.race_lookup[ancestry] = get_key_value(city_ethnicity, ancestry)

        # GENERAL
        self.name = self.cityDict["city"]["name"]
        self.region = self.cityDict["city"]["region"]
        self.alignment = self.cityDict["city"]["alignment"]
        self.cityType = self.cityDict["city"]["type"]
        self.baseValue = int(self.cityDict["city"]["base_value"])
        self.purchaseLimit = int(self.cityDict["city"]["purchase_limit"])
        self.spellcasting = int(self.cityDict["city"]["spellcasting"])
        self.government = self.cityDict["city"]["government"]
        self.population = int(self.cityDict["city"]["population"])
        self.npcs = self.cityDict["city"]["npcs"]
        self.qualities = self.cityDict["city"]["qualities"]

        # MODIFIERS
        self.cityCorruption = int(self.cityDict["city"]["modifiers"]["corruption"])
        self.cityCrime = int(self.cityDict["city"]["modifiers"]["crime"])
        self.cityEconomy = int(self.cityDict["city"]["modifiers"]["economy"])
        self.cityLaw = int(self.cityDict["city"]["modifiers"]["law"])
        self.cityLore = int(self.cityDict["city"]["modifiers"]["lore"])
        self.citySociety = int(self.cityDict["city"]["modifiers"]["society"])
        self.modifierLookup = OrderedDict([("Corruption", self.cityCorruption),
                                           ("Crime", self.cityCrime),
                                           ("Economy", self.cityEconomy),
                                           ("Law", self.cityLaw),
                                           ("Lore", self.cityLore),
                                           ("Society", self.citySociety)])

        # DISADVANTAGES
        try:
            self.disadvantages = self.cityDict["city"]["disadvantages"]
        except KeyError:
            self.disadvantages = None  # Disadvantages are not mandatory

    def _print_city_general_details(self):
        """Print city's details.

        Print the city's name, region, alignment, type, modifiers, qualities, danger, and
        disadvantages.
        """
        # Name
        print_header(self.name.upper())

        # Region
        print("Region {}".format(self.region))

        # Alignment
        # Type
        print("{} {}".format(self.alignment, self.cityType.lower()))

        # Modifiers
        self._print_city_modifiers()

        # Qualities
        self._print_city_qualities()

        # Danger
        # See: Task 10-4

        # Disadvantages
        self._print_city_disadvantages()

        # DONE
        print("")

    def _print_city_modifiers(self):
        # LOCAL VARIABLES
        modifierString = ""

        # PRINT
        for modifier in CITY_MODIFIER_LIST:
            modifierString = modifierString + "{} {:+d}; ".format(modifier,
                                                                  self.modifierLookup[modifier])
        modifierString = modifierString[:len(modifierString)-2]  # Trim off the end
        print(modifierString)

    def _print_city_qualities(self):
        # LOCAL VARIABLES
        qualitiesString = ""

        # PRINT
        for cityQuality in self.qualities:
            qualitiesString = qualitiesString + cityQuality.lower() + ", "
        qualitiesString = qualitiesString[:len(qualitiesString)-2]  # Trim the trailing comma
        print("Qualities {}".format(qualitiesString))

    def _print_city_disadvantages(self):
        # LOCAL VARIABLES
        disadvantagesString = ""

        # PRINT
        if self.disadvantages:
            for cityDisadvantage in self.disadvantages:
                disadvantagesString = disadvantagesString + cityDisadvantage.lower() + ", "
            # Trim the trailing comma
            disadvantagesString = disadvantagesString[:len(disadvantagesString)-2]
            print("Disadvantages {}".format(disadvantagesString))

    def _print_city_demographic_details(self):
        """Print city's government, population, and NPCs"""
        # Header
        print_header("DEMOGRAPHICS")
        # Government
        print(f'Government {self.government}')
        # Population (Ancestry breakdown)
        print(f'Population {self.population} ({self._determine_ancestry_breakdown()})')
        # NPCs
        # self.print_city_npcs()  # TOO VERBOSE
        print("")

    def _determine_ancestry_breakdown(self):
        """Return a city size based list of the top ancestries"""
        # LOCAL VARIABLES
        cityLookup = {
                "Thorp": 2, "Hamlet": 2, "Village": 3, "Small Town": 3,
                "Large Town": 4, "Small City": 4, "Large City": 5, "Metropolis": 5
                }
        numAncestries = cityLookup[self.cityType]
        retStr = None

        # CONSTRUCT STRING
        retStr = self._construct_ancestry_string(numAncestries)

        # DONE
        return retStr

    def _construct_ancestry_string(self, numEntries):
        """Construct a string of the top numEntries ancestries, ending in other"""
        # LOCAL VARIABLES
        ancestryStr = ""
        ancestorDict = {}
        valueList = []
        runningPopTotal = 0

        # CONSTRUCT STRING
        # 1. Calculate populations by ancestry
        for race in ANCESTRY_LIST:
            if race == "Human":
                ancestorDict[race] = self._calc_total_human_population()
            else:
                try:
                    ancestorDict[race] = int(self.cityDict["city"]["ancestry"][race]
                                             * .01 * self.population)
                except KeyError:
                    ancestorDict[race] = 0  # Not found?  They don't live here.

        # 2. Sort populations
        valueList = list(ancestorDict.values())
        valueList.sort(reverse=True)

        # 3. Start forming the string
        for index in range(numEntries):
            if index > len(valueList) - 1:
                break
            ancestryStr = ancestryStr + " " \
                + self._form_one_ancestry_substring(ancestorDict, valueList[index]) + ";"
            # Keep track of the population already accounted for to support "others"
            runningPopTotal += valueList[index]

        # 4. Others
        ancestryStr = ancestryStr + " {} {}".format(self.population - runningPopTotal, "other")

        # 5. Trim
        ancestryStr = ancestryStr[1:]

        # DONE
        return ancestryStr

    def _form_one_ancestry_substring(self, ancestorDict, topValue):
        # LOCAL VARIABLES
        ancestrySubstr = ""

        # CONSTRUCT SUBSTRING
        # Find it
        for dictKey, dictValue in ancestorDict.items():
            if dictValue == topValue:
                ancestrySubstr = "{} {}".format(dictValue, dictKey)
                if dictValue > 1:
                    ancestrySubstr = ancestrySubstr + "s"
            if ancestrySubstr:
                break

        # DONE
        return ancestrySubstr

    def _calc_total_human_population(self):
        """Return the total human population based on cityDict percentages and city population"""
        # LOCAL VARIABLES
        totalHumanPop = 0
        totalHumanPer = 0.0

        # CALCULATE
        # Total Percent
        for ethnicity in self.cityDict["city"]["ancestry"]["Human"]:
            totalHumanPer += self.cityDict["city"]["ancestry"]["Human"][ethnicity]
        # Total Population
        totalHumanPop = int(totalHumanPer * self.population * .01)

        # DONE
        return totalHumanPop

    def _print_city_marketplace_details(self):
        """Print city's base value, purchase limit, spellcasting, and magic items"""
        # LOCAL VARIABLES
        numToWord = inflect.engine()

        # PRINT
        # Header
        print_header("MARKETPLACE")
        # Base Value
        # Purchase Limit
        # Spellcasting
        print(f'Base Value {self.baseValue} gp; Purchase Limit {self.purchaseLimit} gp; '
              f'Spellcasting {numToWord.ordinal(self.spellcasting)}')

        # Magic Items
        # See: Task 5-7
