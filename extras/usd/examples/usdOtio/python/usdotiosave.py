#
# Standard python imports
#
import os

#
# USD imports
#
try:
    from pxr import Usd
except ImportError:
    print(f'''
"pxr" python module not found.  Check PYTHONPATH and LD_LIBRARY_PATH on Linux or
macOS.
Check PATH on Windows.
''', file=sys.stderr)
    exit(1)

#
# OpentimelineIO imports
#
try:
    import opentimelineio as otio
except ImportError:
    print(f'''
Python's opentimelineio module not found!

Please run:
    pip install opentimelineio
''', file=sys.stderr)
    exit(1)

#
# usdOtio helper classes' imports here
#
from usdOtio.options import Options
from usdOtio.clip import Clip
from usdOtio.gap import Gap
from usdOtio.stack import Stack
from usdOtio.timeline import Timeline
from usdOtio.transition import Transition
from usdOtio.options import Options, Verbose
from usdOtio.track import Track
from usdOtio.effect import Effect
    
class UsdOtioSave:
    def __init__(self, usd_file, otio_file, usd_path = '/'):
        self.usd_file = usd_file
        self.otio_file = otio_file
        self.usd_path = usd_path

    def run(self):
        """
        Run the otio save (extract .otio) algorithm.
        """

        #
        # Open the original scene file
        #
        try:
            stage = Usd.Stage.Open(self.usd_file)
        except:
            print(f'ERROR: Could not open USD file {self.usd_file}',
                  file=sys.stderr)
            exit(1)
        #
        # Get an USD otio primitive at path/otio.
        #
        usd_prim = stage.GetPrimAtPath(self.usd_path)
        
        valid_path = True
        if not usd_prim:
            valid_path = False
            print(f'No primitive at USD path "{self.usd_path}"!')
        else: 
            usd_type = usd_prim.GetTypeName()
            if usd_type != 'OtioTimeline':
                valid_path = False
                print(f'''USD path "{self.usd_path}" not an OtioTimeline primitive, 
but type {usd_type}!

''')

        if not valid_path:
            print(f'''
Use -p <path> for passing the path to an already existing OtioTimeline primitive.

Valid OtioTimeline primitives in stage:''')
            found = False
            for x in stage.Traverse():
                if x.GetTypeName() == 'OtioTimeline':
                    print(f'\t{x} is an OtioTimeline primitive.')
                    found = True
            if not found:
                print('\tNone')
            exit(1)

        #
        # Create a timeline and extract the .otio json data from this usd
        # OtioTimeline primitive
        #
        timeline = Timeline()
        json_data = timeline.from_usd(usd_prim)
        #
        # Check if otio file already exists
        #
        if os.path.isfile(self.otio_file):
            if Options.verbose >= Verbose.NORMAL:
                print(f'"{self.otio_file}" already exists!  Will overwrite it.')
                Options.continue_prompt()
        
        #
        # Write out the json data
        #
        if Options.debug:
            with open(self.otio_file, 'w') as f:
                f.write(json_data)
        else:
            timeline = otio.schema.Timeline.from_json_string(json_data)
            timeline.to_json_file(self.otio_file)
