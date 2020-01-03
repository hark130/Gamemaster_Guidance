from GG_Ancestry import GG_Ancestry

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
        # print("User Input: {}".format(userChoice))  # DEBUGGING
    # except Exception as err:
    #     print("Invalid Input: {}".format(err))
    #     raise err
    except:
        userChoice = int(-1)

    return userChoice


def rando_a_name():
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
    userInput = read_user_input()

    try:
        if userInput == 1:
            character = GG_Ancestry()
        elif userInput == 2:
            character = GG_Ancestry(race="Dwarf")
        elif userInput == 3:
            character = GG_Ancestry(race="Elf")
        elif userInput == 4:
            character = GG_Ancestry(race="Gnome")
        elif userInput == 5:
            character = GG_Ancestry(race="Goblin")
        elif userInput == 6:
            character = GG_Ancestry(race="Halfling")
        elif userInput == 7:
            character = GG_Ancestry(race="Human")
        elif userInput == 8:
            character = GG_Ancestry(race="Half-Elf")
        elif userInput == 9:
            character = GG_Ancestry(race="Half-Orc")
        elif userInput == 42:
            return userInput
        else:
            return 999
    except RuntimeError as err:
        print(format(err))
    else:
        if character:
            pass  # TO DO: DON'T DO NOW... Call print method
            print("\n" + character.fullName + "\n")  # Placeholder

    return userInput


def menu():
    clear_screen()
    userInput = 0
    print("\nWelcome to Gamemaster Guidance\n")

    while userInput != 999:
        # print("User Input: {}".format(userInput))  # DEBUGGING
        print("  1. Randomize a name")
        print("999. Exit")
        print("Choose an option [999]:")
        userInput = read_user_input()
        # print("User Input: {}".format(userInput))  # DEBUGGING
        if userInput == 1:
            userInput = rando_a_name()
        else:
            break

    return

def main():
    menu()


if __name__ == "__main__":
    main()
