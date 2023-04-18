def menu():
    """
    Displays the main menu of options to the user.
    """
    print("Welcome to Cloud Infrastructure Hardening")
    print("Please choose an option:")
    print("1. Harden Infrastructure")
    print("2. Apply ISO Standards")
    print("3. Exit")

    # Input validation loop
    while True:
        try:
            choice = int(input())
            if choice < 1 or choice > 3:
                print("Invalid option. Please try again.")
            else:
                return choice
        except ValueError:
            print("Invalid input. Please enter a number.")

In this updated version of the menu function, we've added a try-except block to catch any ValueError exceptions that might be raised if the user inputs a non-numeric value. We've also added a loop that continues to prompt the user for input until a valid option is chosen.

You can apply similar input validation to any other user input in the script to prevent unintended behavior or malicious input.
