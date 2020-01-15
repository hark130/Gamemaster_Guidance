from . GG_Globals import ancestryList, humanEthnicityList
from . GG_Rando import rand_float
from . import GG_Yaml


import locale


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
    supportedQualities = []


    def __init__(self, cityDict):
        """Class constructor"""
        self.cityDict = cityDict

        # Use these attributes to indicate a value should be randomized prior to parsing
        self.randoDisadvantage = False  # Randomize a disadvantage
        self.randoAlignment = False
        self.randoGovernment = False
        self.randoPopulation = False
        self.randoQuality = False


    def load(self):
        """Entry level method: validate and parse the dictionary"""
        self._validate_city()
        self._parse_city()


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
        ethics = ["Lawful", "Neutral", "Chaotic"]
        moralities = ["Good", "Neutral", "Evil"]
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
            except:
                raise RuntimeError("Invalid population")


    def _validate_defined(self):
        """Validate any script-defined entries in cityDict"""
        pass


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










