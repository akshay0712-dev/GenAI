import colorama
from colorama import Fore, Back, Style
import os

colorama.init()

# Configuration
LEFT_MARGIN = "   "  # Adjust the number of spaces for the left margin
BOX_WIDTH = 60

# Clear the terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return Fore.RED + LEFT_MARGIN + "Cannot divide by zero" + Style.RESET_ALL
    return x / y


# Styled Heading
def print_heading():
    heading_text = "CALCULATOR"

    # Larger characters using ASCII art
    large_c = [
        "  ####  ",
        " #    # ",
        " #      ",
        " #      ",
        " #    # ",
        "  ####  "
    ]
    large_a = [
        "  ####  ",
        " #    # ",
        " ###### ",
        " #    # ",
        " #    # ",
        " #    # "
    ]
    large_l = [
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " ###### "
    ]
    large_u = [
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  "
    ]
    large_t = [
        " ###### ",
        "   ##   ",
        "   ##   ",
        "   ##   ",
        "   ##   ",
        "   ##   "
    ]
    large_o = [
        "  ####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  "
    ]
    large_r = [
        "  ####  ",
        " #    # ",
        " ###### ",
        " #   #  ",
        " #    # ",
        " #    # "
    ]

    letters = {
        'C': large_c,
        'A': large_a,
        'L': large_l,
        'U': large_u,
        'T': large_t,
        'O': large_o,
        'R': large_r
    }

    # Print the large heading
    heading_lines = []
    for i in range(6):
        line = LEFT_MARGIN
        for char in heading_text:
            line += Fore.YELLOW + letters[char][i] + Style.RESET_ALL + "  "
        heading_lines.append(line)

    for line in heading_lines:
        print(line)
    print()


def print_menu():
    print(Fore.CYAN + Style.BRIGHT + LEFT_MARGIN + "Select operation:\n" + Style.RESET_ALL)
    print(Fore.GREEN + LEFT_MARGIN + "1. Add" + Style.RESET_ALL)
    print(Fore.GREEN + LEFT_MARGIN + "2. Subtract" + Style.RESET_ALL)
    print(Fore.GREEN + LEFT_MARGIN + "3. Multiply" + Style.RESET_ALL)
    print(Fore.GREEN + LEFT_MARGIN + "4. Divide" + Style.RESET_ALL)
    print(Fore.RED + LEFT_MARGIN + "5. Exit" + Style.RESET_ALL)
    print()


while True:
    clear_terminal()
    print_heading()
    print_menu()

    choice = input(Fore.YELLOW + LEFT_MARGIN + LEFT_MARGIN + "Enter choice (1/2/3/4/5): " + Style.RESET_ALL)

    if choice == '5':
        print(Fore.YELLOW + "\n" + LEFT_MARGIN + LEFT_MARGIN + "Exiting calculator..." + Style.RESET_ALL)
        break

    if choice in ('1', '2', '3', '4'):
        try:
            num1 = float(input(Fore.BLUE + LEFT_MARGIN + LEFT_MARGIN + "Enter first number: " + Style.RESET_ALL))
            num2 = float(input(Fore.BLUE + LEFT_MARGIN + LEFT_MARGIN + "Enter second number: " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "\n" + LEFT_MARGIN + LEFT_MARGIN + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input(LEFT_MARGIN + LEFT_MARGIN + "Press Enter to continue...")  # Pause for user to see the message
            continue

        if choice == '1':
            result = add(num1, num2)
            print(Fore.GREEN + f"\n{LEFT_MARGIN + LEFT_MARGIN}{num1} + {num2} = {result}" + Style.RESET_ALL)

        elif choice == '2':
            result = subtract(num1, num2)
            print(Fore.GREEN + f"\n{LEFT_MARGIN + LEFT_MARGIN}{num1} - {num2} = {result}" + Style.RESET_ALL)

        elif choice == '3':
            result = multiply(num1, num2)
            print(Fore.GREEN + f"\n{LEFT_MARGIN + LEFT_MARGIN}{num1} * {num2} = {result}" + Style.RESET_ALL)

        elif choice == '4':
            result = divide(num1, num2)
            print(Fore.GREEN + f"\n{LEFT_MARGIN + LEFT_MARGIN}{num1} / {num2} = {result}" + Style.RESET_ALL)

        input(LEFT_MARGIN + LEFT_MARGIN + "Press Enter to continue...")  # Pause for user to see the result

    else:
        print(Fore.RED + "\n" + LEFT_MARGIN + LEFT_MARGIN + "Invalid input" + Style.RESET_ALL)
        input(LEFT_MARGIN + LEFT_MARGIN + "Press Enter to continue...")  # Pause for user to see the message