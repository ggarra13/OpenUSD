
from enum import Enum, auto

class Verbose(Enum):
    QUIET   = auto()
    NORMAL  = auto()
    INFO    = auto()
    VERBOSE = auto()
    DEBUG   = auto()
    
    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        return False  # Handle non-enum comparison

class Options:
    #
    # When this is True, we skip all interactive questions in the script 
    #
    yes = False

    #
    #
    #
    verbose = Verbose.NORMAL

    #
    # When this is True, we save the .otio file with python.
    # When it is False, we save it with opentimelineio's python module.
    #
    debug = True

    @staticmethod
    def continue_prompt():
        """
        Prompt user to continue or cancel.
        """
        if Options.yes:
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
