ancestryList = ["Dwarf", "Elf", "Gnome", "Goblin", "Halfling", "Human", "Half-Elf", "Half-Orc"]
cityModifierList = ["Corruption", "Crime", "Economy", "Law", "Lore", "Society"]
citySizeLimits = (5, 200000)  # (Min, Max)
humanEthnicityList = ["Garundi", "Keleshite", "Kellid", "Mwangi", "Nidalese", "Shoanti", "Taldan", "Tian", "Ulfen", "Varisian", "Vudrani"]  # User Story 8. Nidalese
classList = ["Adept", "Alchemist", "Aristocrat", "Barbarian", "Bard", "Champion", "Cleric", "Commoner",
             "Druid", "Expert", "Fighter", "Monk", "Ranger", "Rogue", "Sorcerer", "Warrior", "Wizard"]

def print_header(header):
    # LOCAL VARIABLES
    headerLen = len(header)
    banner = "-" * headerLen

    print(banner)
    print(header)
    print(banner)
