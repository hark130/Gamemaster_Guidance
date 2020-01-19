from . GG_Globals import ancestryList, citySizeLimits, humanEthnicityList
from . GG_Rando import rand_float, rand_integer
from . import GG_Yaml


import inflect
import locale
import math
import random


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
    supportedQualities = ["Academic", "Holy Site", "Insular", "Magically Attuned", "Notorious", "Pious",
                          "Prosperous", "Racially Intolerant", "Rumormongering Citizens",
                          "Strategic Location", "Superstitious", "Tourist Attraction"]
    supportedEthics = ["Lawful", "Neutral", "Chaotic"]
    supportedMoralities = ["Good", "Neutral", "Evil"]
    settlementStatistics = {
        "Thorp":{"Modifiers":-4,"Qualities":1,"Danger":-10,"Base Value":50,"Purchase Limit":500,"Spellcasting":1,"Base Value":50},
        "Hamlet":{"Modifiers":-2,"Qualities":1,"Danger":-5,"Base Value":200,"Purchase Limit":1000,"Spellcasting":2,"Base Value":200},
        "Village":{"Modifiers":-1,"Qualities":2,"Danger":0,"Base Value":500,"Purchase Limit":2500,"Spellcasting":3,"Base Value":500},
        "Small Town":{"Modifiers":0,"Qualities":2,"Danger":0,"Base Value":1000,"Purchase Limit":5000,"Spellcasting":4,"Base Value":1000},
        "Large Town":{"Modifiers":0,"Qualities":3,"Danger":5,"Base Value":2000,"Purchase Limit":10000,"Spellcasting":5,"Base Value":2000},
        "Small City":{"Modifiers":1,"Qualities":4,"Danger":5,"Base Value":4000,"Purchase Limit":25000,"Spellcasting":6,"Base Value":4000},
        "Large City":{"Modifiers":2,"Qualities":5,"Danger":10,"Base Value":8000,"Purchase Limit":50000,"Spellcasting":7,"Base Value":8000},
        "Metropolis":{"Modifiers":4,"Qualities":6,"Danger":10,"Base Value":16000,"Purchase Limit":100000,"Spellcasting":8,"Base Value":16000}
    }


    def __init__(self, cityDict):
        """Class constructor"""
        self.cityDict = cityDict
        self.baseCityModifier = None
        self.npcMultiplier = 1  # Large cities can have multiple high-level NPCs

        # Use these attributes to indicate a value should be randomized prior to parsing
        self.randoDisadvantage = False  # Randomize a disadvantage
        self.randoAlignment = False
        self.randoGovernment = False
        self.randoPopulation = False
        self.randoQuality = False

        # Use these attributes to indicate a value should be calculated prior to parsing
        self.calcBaseValue = False
        self.calcMagicItems = False
        self.calcNPCs = False
        self.calcType = False


    def load(self):
        """Entry level method: validate and parse the dictionary"""
        self._validate_city()  # Verify all input
        # print("ENTERING GG_City.load()")  # DEBUGGING
        self._complete_city()  # Fill in the blanks
        self._parse_city()     # Load the city into attributes


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
        for ancestry in ancestryList:
            temp = self.cityDict["city"]["ancestry"][ancestry]

        self._validate_human_ethnicities()


    def _validate_human_ethnicities(self):
        for ethnicity in humanEthnicityList:
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
        except:
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
        except:
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
        except:
            self.randoGovernment = True
        else:
            if government not in self.supportedGovernments:
                raise RuntimeError("Unsupported government")


    def _validate_population(self):
        try:
            population = self.cityDict["city"]["population"]
        except:
            self.randoPopulation = True
        else:
            try:
                temp = locale.atoi(population)
            except Exception as err:
                print("Invalid population: {}".format(population))
                print(repr(err))
                raise err


    def _validate_qualities(self):
        try:
            qualities = self.cityDict["city"]["qualities"]
        except:
            self.randoQualities = True
            # print("MISSING KEY")  # DEBUGGING
        else:
            if not qualities:
                self.randoQualities = True
                # print("MISSING VALUE")  # DEBUGGING
            else:
                # print(qualities)  # DEBUGGING
                # Respond to type
                if isinstance(qualities, str):
                    qualities = [qualities]
                elif not isinstance(qualities, list):
                    raise TypeError("Unknown qualities entry")
                # Parse entries
                for quality in qualities:
                    if quality not in self.supportedQualities and not quality.startswith("Racially Intolerant"):
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
        except:
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
        except:
            self.calcNPCs = True
        else:
            if not cityNPCs:
                self.calcNPCs = True


    def _validate_city_type(self):
        # Get it
        try:
            localType = self.cityDict["city"]["type"]
        except:
            self.calcType = True
        else:
            if localType not in self.settlementStatistics.keys():
                raise RuntimeError("Invalid city type")

        # print("CALC CITY TYPE IS: {}".format(self.calcType))  # DEBUGGING


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
        self.cityDict["city"]["population"] = str(rand_integer(citySizeLimits[0], citySizeLimits[1]))


    def _rando_disadvantage(self):
        """Randomize one disadvantage into self.cityDict"""
        self.cityDict["city"]["disadvantages"] = [random.choice(self.supportedDisadvantages)]


    def _rando_alignment(self):
        """Randomize one alignment into self.cityDict"""
        # Rando
        localAlignment = random.choice(self.supportedEthics) + " " + random.choice(self.supportedMoralities)
        # Update True Neutral
        if localAlignment == "Neutral Neutral":
            localAlignment = "Neutral"
        # Store It
        self.cityDict["city"]["alignment"] = localAlignment
        # print("CITY ALIGNMENT: {}".format(localAlignment))  # DEBUGGING


    def _rando_government(self):
        """Randomize a government into self.cityDict"""
        self.cityDict["city"]["government"] = random.choice(self.supportedGovernments)
        # print("CITY GOVERNMENT: {}".format(self.cityDict["city"]["government"]))  # DEBUGGING


    def _calculate_city(self):
        """Calculate all the details of a city not already calculated in the config"""
        # Calculate this first since the settlement statistics are derived from it
        # print("CALC CITY TYPE IS: {}".format(self.calcType))  # DEBUGGING
        if self.calcType:
            self._calc_city_type()
            self.calcType = False

        # Moved from _rando_city since the "type" should be defined before the qualities
        if self.randoQualities:
            self._rando_city_qualities()
            self.randoQualities = False

        # print("CALC BASE VALUE: {}".format(self.calcBaseValue))  # DEBUGGING
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
        if self.calcNPCs:
            self._rando_city_npcs()
            self.calcNPCs = False


    def _calc_city_type(self):
        """Calculate and store the city type into cityDict"""
        # Get Population
        population = locale.atoi(self.cityDict["city"]["population"])
        # print("POPULATION: {}".format(population))  # DEBUGGING

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
        assert (localType in self.settlementStatistics.keys()),"Invalid city type"

        # Done
        # print(localType)  # DEBUGGING
        self.cityDict["city"]["type"] = localType


    def _rando_city_qualities(self):
        # LOCAL VARIABLES
        localQualList = []
        tempQual = None
        numQuals = self.settlementStatistics[self.cityDict["city"]["type"]]["Qualities"]

        # INPUT VALIDATION
        assert (numQuals > 0),"Invalid number of qualities"
        assert (numQuals <= len(self.supportedQualities)),"Not enough supported qualities"

        # RANDO QUALITIES
        while len(localQualList) < numQuals:
            tempQual = random.choice(self.supportedQualities)
            if tempQual not in localQualList:
                localQualList.append(tempQual)

        # DONE
        self.cityDict["city"]["qualities"] = localQualList
        # print("QUALITIES: {}".format(localQualList))  # DEBUGGING


    def _calc_city_base_value(self):
        """Calcualte city's base value, adjust for qualities/disadvantages, then store it in city dict"""
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
        except:
            pass  # Disadvantages are not mandatory

        # ADJUST BASE VALUE
        localBaseValue = localBaseValue * adjustPercent * .01

        # DONE
        # print("ADJUST BY {} PERCENTAGE".format(adjustPercent * .01))
        # print("RAW BASE VALUE: {}".format(localBaseValue))  # DEBUGGING
        self.cityDict["city"]["base_value"] = str(int(localBaseValue))
        # print("CITY BASE VALUE: {}".format(self.cityDict["city"]["base_value"]))  # DEBUGGING


    def _calc_city_modifiers(self):
        """Calcualte all six city modifiers into cityDict"""
        #   modifiers:
        self.baseCityModifier = self.settlementStatistics[self.cityDict["city"]["type"]]["Modifiers"]
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
        """Calcualte city's purchase limit, adjust for qualities/disadvantages, then store it in city dict"""
        # LOCAL VARIABLES
        localPurchaseLimit = self.settlementStatistics[self.cityDict["city"]["type"]]["Purchase Limit"]
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
        except:
            pass  # Disadvantages are not mandatory

        # ADJUST BASE LIMIT
        localPurchaseLimit = localPurchaseLimit * adjustPercent * .01

        # DONE
        # print("ADJUST BY {} PERCENTAGE".format(adjustPercent * .01))
        # print("RAW PURCHASE LIMIT: {}".format(localPurchaseLimit))  # DEBUGGING
        self.cityDict["city"]["purchase_limit"] = str(int(localPurchaseLimit))
        # print("CITY PURCHASE LIMIT: {}".format(self.cityDict["city"]["purchase_limit"]))  # DEBUGGING


    def _calc_city_spellcasting(self):
        """Calcualte city's spellcasting, adjust for qualities/disadvantages, then store it in city dict"""
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

        # DONE
        self.cityDict["city"]["spellcasting"] = str(localSpellcasting)
        # print("CITY SPELLCASTING: {}".format(self.cityDict["city"]["spellcasting"]))  # DEBUGGING


    def _rando_city_npcs(self):
        """Randomize NPCs and add them to cityDict as a list"""
        # PREPARE LIST
        self.cityDict["city"]["npcs"] = []

        # UPDATE MULTIPLIER
        self._update_city_npc_multiplier()

        # CALCUALTE NPCs
        # Adept 1d6 + community modifier (Task 5-6)
        # Alchemist 1d4 + community modifier (Class)
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
        # TO DO: DON'T DO NOW...
        # Take the remaining population after all other characters are generated
        # and divide it up so that 91% are commoners, 5% are warriors, 3%
        # are experts, and the remaining 1% is equally divided between
        # aristocrats and adepts (0.5% each)


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


    def _determine_human_ethnic_average(self):
        """Return the average of all human ethnic percentages"""
        # TO DO: DON'T DO NOW... Define this
        return 1.136  # Hard-coded value based on test_city.yml


    def _determine_human_barbarian_average(self):
        """Return the total percent of Kellid and Ulfen ethnic percentages"""
        # TO DO: DON'T DO NOW... Define this
        return 1.136 * 2  # Hard-coded value based on test_city.yml


    def _rando_city_npc_bards(self):
        pass


    def _rando_city_npc_champions(self):
        pass


    def _rando_city_npc_clerics(self):
        pass


    def _rando_city_npc_druids(self):
        pass


    def _rando_city_npc_fighters(self):
        pass


    def _rando_city_npc_monks(self):
        pass


    def _rando_city_npc_rangers(self):
        pass


    def _rando_city_npc_rogues(self):
        pass


    def _rando_city_npc_sorcerers(self):
        pass


    def _rando_city_npc_wizards(self):
        pass


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
            # print("_rando_npc_class ITERATION NUMBER: {}".format(_ + 1))  # DEBUGGING
            numOfThatLevel = 1  # Reset temp variable
            charLevel = self._calc_highest_level(numDice, numFaces)
            # print("HIGHEST LEVEL: {}".format(charLevel))  # DEBUGGING
            levelDict[charLevel] += numOfThatLevel
            while charLevel >= 2:
                charLevel = math.ceil(charLevel / 2)
                numOfThatLevel *= 2
                levelDict[charLevel] += numOfThatLevel
            # print("LEVEL DICTIONARY: {}".format(levelDict))  # DEBUGGING

        print("LEVEL DICTIONARY: {}".format(levelDict))  # DEBUGGING
        self._translate_level_dict_into_npc_list(className, levelDict)


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
        # print(sortedDictKeys)  # DEBUGGING

        for level in sortedDictKeys:
            if levelDict[level] > 0:
                npcListEntry = numToWord.number_to_words(levelDict[level]).capitalize() + " " + numToWord.ordinal(level) + " level " + className
                if levelDict[level] > 1:
                    npcListEntry = npcListEntry + "s"

                # print(npcListEntry)  # DEBUGGING
                self.cityDict["city"]["npcs"].append(npcListEntry)
        # print(self.cityDict["city"]["npcs"])  # DEBUGGING


    def _calc_city_modifier_corruption(self):
        # LOCAL VARIABLES
        localCorruption = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].endswith("Evil"):
            # print("EVIL!")  # DEBUGGING
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
        except:
            pass  # Disadvantages are not mandatory
        # print("CORRUPTION: {}".format(localCorruption))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"corruption":str(localCorruption)})


    def _calc_city_modifier_crime(self):
        # LOCAL VARIABLES
        localCrime = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].startswith("Chaotic"):
            # print("CHAOTIC!")  # DEBUGGING
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
        except:
            pass  # Disadvantages are not mandatory
        # print("CRIME: {}".format(localCrime))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"crime":str(localCrime)})


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
        except:
            pass  # Disadvantages are not mandatory
        # print("ECONOMY: {}".format(localEconomy))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"economy":str(localEconomy)})


    def _calc_city_modifier_law(self):
        # LOCAL VARIABLES
        localLaw = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].startswith("Lawful"):
            # print("LAWFUL!")  # DEBUGGING
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
        except:
            pass  # Disadvantages are not mandatory
        # print("LAW: {}".format(localLaw))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"law":str(localLaw)})


    def _calc_city_modifier_lore(self):
        # LOCAL VARIABLES
        localLore = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"] == "Neutral":
            # print("NEUTRAL!")  # DEBUGGING
            localLore += 2
        elif self.cityDict["city"]["alignment"].endswith("Neutral"):
            # print("NEUTRAL")  # DEBUGGING
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
        # print("LORE: {}".format(localLore))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"lore":str(localLore)})


    def _calc_city_modifier_society(self):
        # LOCAL VARIABLES
        localSociety = self.baseCityModifier

        # Alignment
        if self.cityDict["city"]["alignment"].endswith("Good"):
            # print("GOOD")  # DEBUGGING
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
        except:
            pass  # Disadvantages are not mandatory
        # print("SOCIETY: {}".format(localSociety))  # DEBUGGING

        # DONE
        self.cityDict["city"]["modifiers"].update({"society":str(localSociety)})


    def _parse_city(self):
        """Parse the cityDict contents into attributes"""
        detailsDict = self.cityDict[GG_Yaml.GG_CITY_KEY]
        cityEthnicity = detailsDict[GG_Yaml.GG_CITY_RACE_KEY]

        self.name = detailsDict[GG_Yaml.GG_CITY_NAME_KEY]
        self.region = detailsDict[GG_Yaml.GG_CITY_REGION_KEY]
        self.dwarfPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_DWARF)
        self.elfPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_ELF)
        self.gnomePercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_GNOME)
        self.goblinPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_GOBLIN)
        self.halflingPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_HALFLING)
        self.garundiPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_GARUNDI)
        self.keleshitePercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_KELESHITE)
        self.kellidPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_KELLID)
        self.mwangiPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_MWANGI)
        self.nidalesePercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_NIDALESE)
        self.shoantiPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_SHOANTI)
        self.taldanPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_TALDAN)
        self.tianPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_TIAN)
        self.ulfenPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_ULFEN)
        self.varisianPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_VARISIAN)
        self.vudraniPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_VUDRANI)
        self.halfElfPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_HALF_ELF)
        self.halfOrcPercent = get_key_value(cityEthnicity, GG_Yaml.GG_CITY_RACE_HALF_ORC)

        self.raceLookup = {
            GG_Yaml.GG_CITY_RACE_DWARF:self.dwarfPercent,
            GG_Yaml.GG_CITY_RACE_ELF:self.elfPercent,
            GG_Yaml.GG_CITY_RACE_GNOME:self.gnomePercent,
            GG_Yaml.GG_CITY_RACE_GOBLIN:self.goblinPercent,
            GG_Yaml.GG_CITY_RACE_HALFLING:self.halflingPercent,
            GG_Yaml.GG_CITY_RACE_GARUNDI:self.garundiPercent,
            GG_Yaml.GG_CITY_RACE_KELESHITE:self.keleshitePercent,
            GG_Yaml.GG_CITY_RACE_KELLID:self.kellidPercent,
            GG_Yaml.GG_CITY_RACE_MWANGI:self.mwangiPercent,
            GG_Yaml.GG_CITY_RACE_NIDALESE:self.nidalesePercent,
            GG_Yaml.GG_CITY_RACE_SHOANTI:self.shoantiPercent,
            GG_Yaml.GG_CITY_RACE_TALDAN:self.taldanPercent,
            GG_Yaml.GG_CITY_RACE_TIAN:self.tianPercent,
            GG_Yaml.GG_CITY_RACE_ULFEN:self.ulfenPercent,
            GG_Yaml.GG_CITY_RACE_VARISIAN:self.varisianPercent,
            GG_Yaml.GG_CITY_RACE_VUDRANI:self.vudraniPercent,
            GG_Yaml.GG_CITY_RACE_HALF_ELF:self.halfElfPercent,
            GG_Yaml.GG_CITY_RACE_HALF_ORC:self.halfOrcPercent
        }


    def get_race_percent(self, raceName):
        """Return a race's percent"""
        return self.raceLookup[raceName]


    def rando_city_race(self):
        # LOCAL VARIABLES
        totalPercent = float(0.0)
        randoRace = None

        # DETERMINE RACE
        # Add total percents
        for percentValue in self.raceLookup.values():
            totalPercent += percentValue
        if totalPercent <= 0.0:
            raise RuntimeError("Race percentages not found")
        # Rando a number
        randoPercent = rand_float(0.0, totalPercent)
        # Find the match
        totalPercent = 0.0
        for race, percent in self.raceLookup.items():
            totalPercent += percent
            if randoPercent <= totalPercent:
                randoRace = race
                break

        # DONE
        if not randoRace:
            raise RuntimeError("Race not found")
        return randoRace
