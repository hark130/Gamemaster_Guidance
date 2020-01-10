from . import GG_Yaml


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
