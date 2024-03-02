
class Options:
    yes = False
    verbose = False

    @staticmethod
    def continue_prompt():
        """
        Prompt user to continue or cancel.
        """
        if Options.yes:
            print("\nShall I continue (y/n)? ")
            print('y\n')
            return
        response = input("\nShall I continue (y/n)? ")
        if response.lower() == 'y':
            return
        elif response.lower() == 'n':
            print('Aborting...')
            exit(1)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            Options.continue_prompt()
