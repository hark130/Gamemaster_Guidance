from . GG_Ancestry import GG_Ancestry
from . GG_Character import GG_Character
from . GG_City import GG_City

import platform
import subprocess


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


def rando_a_character(cityObj=None):
    print_race_menu()
    userInput = read_user_input()

    try:
        if userInput == 1:
            character = GG_Character(cityObject=cityObj)
        elif userInput == 2:
            character = GG_Character(race="Dwarf")
        elif userInput == 3:
            character = GG_Character(race="Elf")
        elif userInput == 4:
            character = GG_Character(race="Gnome")
        elif userInput == 5:
            character = GG_Character(race="Goblin")
        elif userInput == 6:
            character = GG_Character(race="Halfling")
        elif userInput == 7:
            character = GG_Character(race="Human")
        elif userInput == 8:
            character = GG_Character(race="Half-Elf")
        elif userInput == 9:
            character = GG_Character(race="Half-Orc")
        elif userInput == 42:
            return userInput
        else:
            return 999
    except RuntimeError as err:
        print(format(err))
    else:
        if character:
            character.print_character()


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
            return 999
    except RuntimeError as err:
        print(format(err))
    else:
        if charName:
            print("\n" + charName.return_full_name() + "\n")

    return userInput


def menu(cityDict=None):
    clear_screen()
    userInput = 0
    cityObj = None

    if cityDict:
        cityObj = GG_City(cityDict)
        cityObj.load()

    print("\nWelcome to Gamemaster Guidance\n")

    while userInput != 999:
        print("  1. Randomize a name")
        print("  2. Randomize a character")
        print("999. Exit")
        print("Choose an option [999]:")
        userInput = read_user_input()
        if userInput == 1:
            userInput = rando_a_name()
        elif userInput == 2:
            userInput = rando_a_character(cityObj)
        else:
            break

    return
