# Standard Imports
import subprocess

# Third Party Imports
import platform

# Local Imports
from . GG_Ancestry import GG_Ancestry
from . GG_Bounty import GG_Bounty
from . GG_Character import GG_Character
from . GG_City import GG_City


def clear_screen():
    osName = platform.system()
    if osName is "Linux" or osName is "Darwin":
        command = "clear"
    elif osName is "Windows":
        command = "cls"
    else:
        for _ in range(0, 60):
            print("\n")
        return

    subprocess.call([command], shell=True)


def read_user_input():
    """Read an integer from user input.  Return -1 on error"""
    userInput = input()
    try:
        userChoice = int(userInput)
    except:
        userChoice = int(-1)

    return userChoice


def print_race_menu():
    print("\n")
    print("  1. Random race")
    print("  2. Dwarf")
    print("  3. Elf")
    print("  4. Gnome")
    print("  5. Goblin")
    print("  6. Halfling")
    print("  7. Human")
    print("  8. Half-Elf")
    print("  9. Half-Orc")
    print(" 42. Main Menu")
    print("999. Exit")
    print("Choose an option [999]:")


def rando_a_name():
    print_race_menu()
    userInput = read_user_input()

    try:
        if userInput == 1:
            charName = GG_Ancestry()
        elif userInput == 2:
            charName = GG_Ancestry(race="Dwarf")
        elif userInput == 3:
            charName = GG_Ancestry(race="Elf")
        elif userInput == 4:
            charName = GG_Ancestry(race="Gnome")
        elif userInput == 5:
            charName = GG_Ancestry(race="Goblin")
        elif userInput == 6:
            charName = GG_Ancestry(race="Halfling")
        elif userInput == 7:
            charName = GG_Ancestry(race="Human")
        elif userInput == 8:
            charName = GG_Ancestry(race="Half-Elf")
        elif userInput == 9:
            charName = GG_Ancestry(race="Half-Orc")
        elif userInput == 42:
            return userInput
        else:
            raise SystemExit("Exiting Gamemaster Guidance")
    except RuntimeError as err:
        print(format(err))
        raise err
    else:
        if charName:
            print("\n" + charName.return_full_name() + "\n")

    return userInput


def rando_a_character(cityObj=None):
    print_race_menu()
    userInput = read_user_input()

    try:
        if userInput == 1:
            character = GG_Character(cityObject=cityObj)
        elif userInput == 2:
            character = GG_Character(race="Dwarf", cityObject=cityObj)
        elif userInput == 3:
            character = GG_Character(race="Elf", cityObject=cityObj)
        elif userInput == 4:
            character = GG_Character(race="Gnome", cityObject=cityObj)
        elif userInput == 5:
            character = GG_Character(race="Goblin", cityObject=cityObj)
        elif userInput == 6:
            character = GG_Character(race="Halfling", cityObject=cityObj)
        elif userInput == 7:
            character = GG_Character(race="Human", cityObject=cityObj)
        elif userInput == 8:
            character = GG_Character(race="Half-Elf", cityObject=cityObj)
        elif userInput == 9:
            character = GG_Character(race="Half-Orc", cityObject=cityObj)
        elif userInput == 42:
            return userInput
        else:
            raise SystemExit("Exiting Gamemaster Guidance")
    except RuntimeError as err:
        print(format(err))
    else:
        if character:
            character.print_character()


def print_bounty_menu():
    print("\n")
    print("  1. Choose bounty's minimum level")
    print("  2. Choose bounty's race")
    print("  3. Clear screen")
    print(" 42. Main Menu")
    print("999. Exit")
    print("Choose an option [999]:")


def rando_a_bounty_level(cityObj=None):
    print("\nEnter bounty's minimum level:")
    minimumLevel = read_user_input()

    if minimumLevel < 1:
        raise RuntimeError("Level too low")
    elif minimumLevel > 20:
        raise RuntimeError("Level too high")

    try:
        bounty = GG_Bounty(cityObject=cityObj, minLevel=minimumLevel)
    except RuntimeError as err:
        print(format(err))
        bounty = None

    return bounty

def rando_a_bounty_race(cityObj=None):
    print_race_menu()
    userInput = read_user_input()

    try:
        if userInput == 1:
            bounty = GG_Bounty(cityObject=cityObj)
        elif userInput == 2:
            bounty = GG_Bounty(race="Dwarf", cityObject=cityObj)
        elif userInput == 3:
            bounty = GG_Bounty(race="Elf", cityObject=cityObj)
        elif userInput == 4:
            bounty = GG_Bounty(race="Gnome", cityObject=cityObj)
        elif userInput == 5:
            bounty = GG_Bounty(race="Goblin", cityObject=cityObj)
        elif userInput == 6:
            bounty = GG_Bounty(race="Halfling", cityObject=cityObj)
        elif userInput == 7:
            bounty = GG_Bounty(race="Human", cityObject=cityObj)
        elif userInput == 8:
            bounty = GG_Bounty(race="Half-Elf", cityObject=cityObj)
        elif userInput == 9:
            bounty = GG_Bounty(race="Half-Orc", cityObject=cityObj)
        elif userInput == 42:
            return None
        else:
            raise SystemExit("Exiting Gamemaster Guidance")
    except RuntimeError as err:
        print(format(err))
        bounty = None

    return bounty


def rando_a_bounty(cityObj=None):
    print_bounty_menu()
    userInput = read_user_input()
    bounty = None

    try:
        if userInput == 1:
            bounty = rando_a_bounty_level(cityObj)
        elif userInput == 2:
            bounty = rando_a_bounty_race(cityObj)
        elif userInput == 3:
            clear_screen()
        elif userInput == 42:
            bounty = None
        else:
            raise SystemExit("Exiting Gamemaster Guidance")
    except RuntimeError as err:
        print(format(err))
    else:
        if bounty:
            clear_screen()
            bounty.print_all_details()

def print_city_menu():
    print("\n")
    print("  1. Print the city details")
    print("  2. Print the NPCs")
    print("  3. Clear screen")
    print(" 42. Main Menu")
    print("999. Exit")
    print("Choose an option [999]:")


def city_menu(cityObj):
    clear_screen()
    userInput = None  # Stores user input

    while userInput != 999:
        print_city_menu()
        userInput = read_user_input()
        if userInput == 1:
            if cityObj:
                clear_screen()
                cityObj.print_city_details()
            else:
                print("\nNo city config provided")
                return 999
        elif userInput == 2:
            if cityObj:
                clear_screen()
                cityObj.print_city_npcs()
            else:
                print("\nNo city config provided")
                return 999
        elif userInput == 3:
            clear_screen()
        elif userInput == 42:
            return userInput
        else:
            return 999


def menu(cityDict=None):
    clear_screen()
    userInput = 0
    cityObj = None

    if cityDict:
        cityObj = GG_City(cityDict)
        cityObj.load()

    print("\nWelcome to Gamemaster Guidance")

    while userInput != 999:
        print("\n")
        print("  1. Randomize a name")
        print("  2. Randomize a character")
        print("  3. Randomize a bounty")
        print("  4. City menu")
        print("  5. Clear screen")
        print("999. Exit")
        print("Choose an option [999]:")
        userInput = read_user_input()
        if userInput == 1:
            userInput = rando_a_name()
        elif userInput == 2:
            userInput = rando_a_character(cityObj)
        elif userInput == 3:
            userInput = rando_a_bounty(cityObj)
        elif userInput == 4:
            userInput = city_menu(cityObj)
        elif userInput == 5:
            clear_screen()
        else:
            raise SystemExit("Exiting Gamemaster Guidance")
