from . GG_Globals import ancestryList, citySizeLimits, humanEthnicityList
from . GG_Rando import rand_float, rand_integer
from . import GG_Yaml


import locale
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

        # Use these attributes to indicate a value should be randomized prior to parsing
        self.randoDisadvantage = False  # Randomize a disadvantage
        self.randoAlignment = False
        self.randoGovernment = False
        self.randoPopulation = False
        self.randoQuality = False

        # Use these attributes to indicate a value should be calculated prior to parsing
        self.calcBaseValue = False
        self.calcMagicItems = False
        self.calcModifiers = False
        self.calcNPCs = False
        self.calcPurchaseLimit = False
        self.calcSpellcasting = False
        self.calcType = False


    def load(self):
        """Entry level method: validate and parse the dictionary"""
        self._validate_city()  # Verify all input
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
            print("MISSING KEY")  # DEBUGGING
        else:
            if not qualities:
                self.randoQualities = True
                print("MISSING VALUE")  # DEBUGGING
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
        # NOTE: I think I want to REcalculate all modifiers regardless of what's in the config file

        # NPCs

        # Purchase Limit

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


    def _rando_government(self):
        """Randomize a government into self.cityDict"""
        self.cityDict["city"]["government"] = random.choice(self.supportedGovernments)


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

        if self.calcBaseValue:
            self._calc_city_base_value()
            self.calcBaseValue = False

        if self.calcMagicItems:
            # TO DO: DON'T DO NOW
            # IDEAS:
            # 1. Put it into self.settlementStatistics
            # 2. Hard code some responses into a method
            self.calcMagicItems = False

        if self.calcModifiers:
            self.calcModifiers = False

        if self.calcNPCs:
            self.calcNPCs = False

        if self.calcPurchaseLimit:
            self.calcPurchaseLimit = False

        if self.calcSpellcasting:
            self.calcSpellcasting = False


    def _calc_city_type(self):
        """Calculate and store the city type into cityDict"""
        # Get Population
        population = locale.atoi(self.cityDict["city"]["population"])
        print("POPULATION: {}".format(population))  # DEBUGGING

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
        print(localType)  # DEBUGGING
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
        print("QUALITIES: {}".format(localQualList))


    def _calc_city_base_value(self):
        self.cityDict["city"]["base_value"] = str(self.settlementStatistics[self.cityDict["city"]["type"]]["Base Value"])
        print("CITY BASE VALUE: {}".format(self.cityDict["city"]["base_value"]))  # DEBUGGING


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










