ancestryList = ["Dwarf", "Elf", "Gnome", "Goblin", "Halfling", "Human", "Half-Elf", "Half-Orc"]
cityModifierList = ["Corruption", "Crime", "Economy", "Law", "Lore", "Society"]
citySizeLimits = (5, 200000)  # (Min, Max)
GG_CITY_KEY = "city"
GG_CITY_NAME_KEY = "name"
GG_CITY_REGION_KEY = "region"
GG_CITY_RACE_KEY = "ancestry"
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
humanEthnicityList = [GG_CITY_RACE_GARUNDI, GG_CITY_RACE_KELESHITE, GG_CITY_RACE_KELLID, GG_CITY_RACE_MWANGI,
                      GG_CITY_RACE_NIDALESE, GG_CITY_RACE_SHOANTI, GG_CITY_RACE_TALDAN, GG_CITY_RACE_TIAN,
                      GG_CITY_RACE_ULFEN, GG_CITY_RACE_VARISIAN, GG_CITY_RACE_VUDRANI]  # User Story 8. Nidalese
classList = ["Adept", "Alchemist", "Aristocrat", "Barbarian", "Bard", "Champion", "Cleric", "Commoner",
             "Druid", "Expert", "Fighter", "Monk", "Ranger", "Rogue", "Sorcerer", "Warrior", "Wizard"]

def print_header(header):
    # LOCAL VARIABLES
    headerLen = len(header)
    banner = "-" * headerLen

    print(banner)
    print(header)
    print(banner)
