# Copyright 2024 Gonzalo Garramuño for Signly
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
#

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
    debug = False

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
