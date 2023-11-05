"""Defines package-wide values."""

# Standard
from typing import Final, List
# Third Party
# Local

CITY_MODIFIER_LIST: Final[List] = ['Corruption', 'Crime', 'Economy', 'Law', 'Lore', 'Society']
CITY_SIZE_LIMITS: Final[tuple] = (5, 200000)  # (Min, Max)
GG_CITY_KEY: Final[str] = 'city'
GG_CITY_NAME_KEY: Final[str] = 'name'
GG_CITY_REGION_KEY: Final[str] = 'region'
GG_CITY_RACE_KEY: Final[str] = 'ancestry'
GG_CITY_RACE_DWARF: Final[str] = 'Dwarf'
GG_CITY_RACE_ELF: Final[str] = 'Elf'
GG_CITY_RACE_GNOME: Final[str] = 'Gnome'
GG_CITY_RACE_GOBLIN: Final[str] = 'Goblin'
GG_CITY_RACE_HALFLING: Final[str] = 'Halfling'
GG_CITY_RACE_HUMAN: Final[str] = 'Human'
GG_CITY_RACE_GARUNDI: Final[str] = 'Garundi'
GG_CITY_RACE_KELESHITE: Final[str] = 'Keleshite'
GG_CITY_RACE_KELLID: Final[str] = 'Kellid'
GG_CITY_RACE_MWANGI: Final[str] = 'Mwangi'
GG_CITY_RACE_NIDALESE: Final[str] = 'Nidalese'
GG_CITY_RACE_SHOANTI: Final[str] = 'Shoanti'
GG_CITY_RACE_TALDAN: Final[str] = 'Taldan'
GG_CITY_RACE_TIAN: Final[str] = 'Tian'
GG_CITY_RACE_ULFEN: Final[str] = 'Ulfen'
GG_CITY_RACE_VARISIAN: Final[str] = 'Varisian'
GG_CITY_RACE_VUDRANI: Final[str] = 'Vudrani'
GG_CITY_RACE_HALF_ELF: Final[str] = 'Half-Elf'
GG_CITY_RACE_HALF_ORC: Final[str] = 'Half-Orc'
GG_CITY_RACE_TENGU: Final[str] = 'Tengu'
HUMAN_ETHNICITY_LIST: Final[List] = [GG_CITY_RACE_GARUNDI, GG_CITY_RACE_KELESHITE,
                                     GG_CITY_RACE_KELLID, GG_CITY_RACE_MWANGI,
                                     GG_CITY_RACE_NIDALESE, GG_CITY_RACE_SHOANTI,
                                     GG_CITY_RACE_TALDAN, GG_CITY_RACE_TIAN,
                                     GG_CITY_RACE_ULFEN, GG_CITY_RACE_VARISIAN,
                                     GG_CITY_RACE_VUDRANI]  # User Story 8. Nidalese
ANCESTRY_LIST: Final[List] = sorted([GG_CITY_RACE_DWARF, GG_CITY_RACE_ELF, GG_CITY_RACE_GNOME,
                                     GG_CITY_RACE_GOBLIN, GG_CITY_RACE_HALFLING,
                                     GG_CITY_RACE_HUMAN, GG_CITY_RACE_HALF_ELF,
                                     GG_CITY_RACE_HALF_ORC, GG_CITY_RACE_TENGU])
CLASS_LIST: Final[List] = ['Adept', 'Alchemist', 'Aristocrat', 'Barbarian', 'Bard', 'Champion',
                           'Cleric', 'Commoner', 'Druid', 'Expert', 'Fighter', 'Monk', 'Ranger',
                           'Rogue', 'Sorcerer', 'Warrior', 'Wizard']


def print_header(header):
    """Print a header surrounded by a standardized banner."""
    # LOCAL VARIABLES
    banner = '-' * len(header)

    print(banner)
    print(header)
    print(banner)
