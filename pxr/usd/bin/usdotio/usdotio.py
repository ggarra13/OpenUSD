#!/pxrpythonsubst
#
# Copyright 2024 Gonzalo Garramuño
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

#
# Python standard imports
#
import sys, os
import argparse

#
# Instead of relying in the user environment being set, we will modify this
# from within python so that the script will work fine in all OSes.
#
script_dir = os.path.dirname(os.path.abspath(__file__))

# Split the path based on the directory separator
path_parts = script_dir.split(os.path.sep)

# Remove the last element from the path_parts list
path_parts.pop()

# Join the remaining parts back together to form the new path
install_path = os.path.sep.join(path_parts)

#
# Otio plugin dir
#
share_parts = [install_path, 'share', 'usd', 'examples', 'plugin', 'usdOtio']
otio_plugin_dir = os.path.sep.join(share_parts)

#
# Add usdOtio directory to PXR_PLUGINPATH_NAME
#
plugin_path = os.environ.get('PXR_PLUGINPATH_NAME', '')
os.environ['PXR_PLUGINPATH_NAME'] = plugin_path + os.pathsep + otio_plugin_dir

#
# Usd python dir
#
usd_python_parts = [install_path, 'lib', 'python']
usd_python_path = os.path.sep.join(usd_python_parts)

#
# Modify sys.path
# 
sys.path.insert(0, otio_plugin_dir)
sys.path.insert(0, usd_python_path)

#
# USD imports
#
from pxr import Usd

#
# @todo: USDOtio helper classes' imports here 
#


class UsdOtio:
    """
    Class to add or extract an .otio json data file from a .usd fle
    """
    def __init__(self):
        self.parse_arguments()
        self.run()

    def run(self):
        """
        Run the conversion
        """
        if self.mode == 'add':
            self.run_otio_add()
        elif self.mode == 'save':
            self.run_otio_save()
        else:
            raise RuntimeError('Uninplemented mode yet - Patches welcome!')
        
    def run_otio_save(self):
        """
        Run the otio add algorithm.
        """
        #
        # Open the original scene file
        # 
        stage = Usd.Stage.Open(self.usd_file)

        usd_path = self.path + 'otio'

        #
        # Get primitive at path
        #
        otio_prim = stage.GetPrimAtPath(usd_path)
        if not otio_prim:
            print(f'Invalid USD path "{usd_path}" for Otio primitive!')
            print('Use -p <path> for passing the path to the root '
                  'containing Otio primitive "otio".')
            exit(1)

        #
        # Check we have an Otio primitive
        #
        prim_type = otio_prim.GetTypeName()
        if prim_type != 'Otio':
            print(f'Invalid Otio primitive type. Is {prim_type}. ')
            exit(1)

        json_data = otio_prim.GetAttribute('jsonData').Get()

        #
        # Check if otio file already exists
        #
        if os.path.isfile(self.otio_file):
            print(f'{self.otio_file} already exists.  Will overwrite it.')
            self.continue_prompt()
        
        #
        # Write out the json data
        #
        with open(self.otio_file, 'w') as f:
            f.write(json_data)

        if self.verbose:
            print('Extracted:\n\n', json_data)
        
    def run_otio_add(self):
        """
        Run the otio add algorithm.
        """

        #
        # Open the original scene file
        # 
        stage = Usd.Stage.Open(self.usd_file)

        #
        # Create an USD otio primitive at path/otio.
        #
        otio_path = self.path + 'otio'
        otio_prim = stage.DefinePrim(otio_path, 'Otio')

        #
        # Check if we have opentimelineio python library to validate otio
        #
        try:
            validate_otio = True
            import opentimelineio as otio
        except ImportError:
            print("WARNING: Not validating .otio data!")
            validate_otio = False
                
        #
        # Try to validate the otio file
        #
        if validate_otio:
            try:
                timeline = otio.adapters.read_from_file(self.otio_file)
            except:
                print("ERROR: Invalid .otio file or could not convert with installed adapters")
                exit(1)
            json_data = timeline.to_json_string()
        else:
            # Read the JSON data from file
            with open(self.otio_file, "r") as f:
                json_data = f.read()

        #
        # Verify the jsonData attribute is empty
        #
        old_data = otio_prim.GetAttribute('jsonData').Get()
        if old_data and old_data != "Missing .otio's jsonData!":
            print(f'\n\nWarning jsonData for {otio_path} is not empty:')
            print(f'{old_data[:75]}...')
            self.continue_prompt()
            
        #
        # Attach the json data to the otio primitive
        #
        otio_prim.GetAttribute('jsonData').Set(json_data)
        
        #
        # Export modified stage to output file
        #
        stage.Export(self.output_file)

    def parse_arguments(self):
        """
        Parse the command-line's arguments
        """
    
        description="""
        A program to embed and extract an .otio file from a .usd file and to
        convert Omniverse's sequencer to an .usd file with embedded .otio
        data.
        """
            
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Enable verbose mode.')
        subparsers = parser.add_subparsers(dest='mode',
                                           help='Mode of operation')
        parser.add_argument('usd_file', type=str, help='Name of .usd file to add or extract otio data')
        parser.add_argument('-o', '--usd-output-file', type=str, nargs='?',
                            help='USD output file.  '
                            'If no output file is provided, defaults to'
                            'overwrite the same usd file.')
        
            
        

        #
        # 'add' parser
        #
        add_parser = subparsers.add_parser('add', help='Add mode')
        
        add_parser.add_argument('-p', '--usd-path', type=str, nargs='?',
                                const='/', 
                                help='USD path to attach or extract .otio '
                                'primitive to.  If no path provides, defaults '
                                'to "/".')
        add_parser.add_argument('otio_file', type=str, help='Name of .otio file to add or save.')

        #
        # 'save' parser
        #
        save_parser = subparsers.add_parser('save', help='Save mode')
        save_parser.add_argument('-p', '--usd-path', type=str, nargs='?',
                                 const='/', 
                                 help='USD path to attach or extract .otio '
                                 'primitive to.  If no path provides, defaults '
                                 'to "/".')
        save_parser.add_argument('otio_file', type=str, help='Name of .otio file to add or save.')
        
        #
        # 'v2' parser
        #
        v2_parser = subparsers.add_parser('v2', help='Omniverse v2 sequencer to .otio conversion mode')
        
        args = parser.parse_args()

        #
        # Copy arguments to class
        #
        self.verbose = args.verbose
        self.mode = args.mode
        self.usd_file  = args.usd_file
        self.output_file = args.usd_output_file
        self.path = None

        if args.mode != 'v2':
            self.path = args.path
            self.otio_file = args.otio_file
            
        if not self.output_file:
            self.output_file = self.usd_file
        
        if self.verbose:
            print('Verbose mode enabled!')
            print(f'Selected mode: {self.mode}')
                
        if self.path:
            #
            # Sanitize path for usd
            #
            if self.path[0] != '/':
                self.path = '/' + self.path
            if self.path[-1] != '/':
                self.path += '/'
                
            if self.mode == "add":
                print(f"Trying to add {self.otio_file} to {self.usd_file}, USD path {self.path}...")
                print(f'Saving to {self.output_file}')
            elif self.mode == 'save':
                print(f"Trying to get otio data from USD path {self.path}...")

        else:
            self.path = '/'

    def continue_prompt(self):
        """
        Prompt user to continue or cancel.
        """
        response = input("\nShall I continue (y/n)? ")
        if response.lower() == 'y':
            return
        elif response.lower() == 'n':
            print('Aborting...')
            exit(1)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            self.continue_prompt()

if __name__ == '__main__':
    usd_otio = UsdOtio()
    exit(0)
    
