from . import GG_Yaml
from . GG_Rando import rand_float


def get_key_value(theDict, theKey):
    """Returns the key value as a float, 0.0 on Exception"""
    try:
        theValue = float(theDict[theKey])
    except Exception:
        theValue = float(0.0)

    return theValue


class GG_City:


    def __init__(self, cityDict):
        """Class constructor"""
        self.cityDict = cityDict


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
        pass


    def _validate_optional(self):
        """Validate any optional entries in cityDict"""
        pass


    def _validate_defined(self):
        """Validate any script-defined entries in cityDict"""
        pass


    def _parse_city(self):
        """Parse the cityDict contents into attributes"""
        detailsDict = cityDict[GG_Yaml.GG_CITY_KEY]
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










