import yaml


GG_CITY_KEY = "city"
GG_CITY_NAME_KEY = "name"
GG_CITY_REGION_KEY = "region"
GG_CITY_RACE_KEY = "ethnicity"
GG_CITY_RACE_DWARF = "Dwarf"
GG_CITY_RACE_ELF = "Elf"
GG_CITY_RACE_GNOME = "Gnome"
GG_CITY_RACE_GOBLIN = "Goblin"
GG_CITY_RACE_HALFLING = "Halfling"
GG_CITY_RACE_HUMAN = "Human"
GG_CITY_RACE_GARUNDI = "Garundi"
GG_CITY_RACE_KELESHITE = "Keleshite"
GG_CITY_RACE_KELLID = "Kellid"
GG_CITY_RACE_MWANGI = "Mwangi"
GG_CITY_RACE_NIDALESE = "Nidalese"
GG_CITY_RACE_SHOANTI = "Shoanti"
GG_CITY_RACE_TALDAN = "Taldan"
GG_CITY_RACE_TIAN = "Tian"
GG_CITY_RACE_ULFEN = "Ulfen"
GG_CITY_RACE_VARISIAN = "Varisian"
GG_CITY_RACE_VUDRANI = "Vudrani"
GG_CITY_RACE_HALF_ELF = "Half-Elf"
GG_CITY_RACE_HALF_ORC = "Half-Orc"


def parse_yaml(filename):
    yamlDict = None

    try:
        with open(filename, "r") as inFile:
            yamlDict = yaml.load(inFile, Loader=yaml.FullLoader)
    except Exception as err:
        print(format(err))  # DEBUGGING

    return yamlDict
