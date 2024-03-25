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


#
# Normal python imports
#
import sys, os

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
    import opentimelineio.opentime as otime
except ImportError:
    print(f'''
Python's opentimelineio module not found!

Please run:
    pip install opentimelineio
''', file=sys.stderr)
    exit(1)
        
#
# usdotio helper classes' imports here
#
from usdotio.schema.options import Options, LogLevel
from usdotio.schema.clip import Clip
from usdotio.schema.gap import Gap
from usdotio.schema.stack import Stack
from usdotio.schema.timeline import Timeline
from usdotio.schema.track import Track
from usdotio.schema.functions import *
from usdotio.usdotioadd import UsdOtioAdd


    
    
class UsdOtioUpdate:
    """A class to update an .usd file with sequencer information to a .usd
    file with an .otio Timeline.
    """
    def __init__(self, usd_file, output_file, path = '/', comment = True):
        """Constructor

        Args:
        usd_file (str): A valid .usd file with Sequencer information.
        output_file (str): Name of the output .usd file.
        path (str): USD path to attach the otio information to.
        comment (bool): Whether the output .usd file has a comment at the 
                        beginning.  For unit tests, you will want to
                        disable the comments.
        """

        #
        # Store these for easy access.
        #
        self.usd_file = usd_file
        self.output_file = output_file
        self.path = path
        self.comment = not comment
        self.timeline = None
        self.tracks   = []
        self.asset_clip = None

        #
        # USD classes and properties
        #
        self.usd_sequence = None
        self.startTimecode = 1
        self.endTimecode = 1000
        self.fps = 24.0
        
        
    def process_asset(self, stage, asset_path, asset_prim):
        pass
        
    def process_asset_clip(self, stage, track_path, asset_clip_prim):
        startTime = get_timecode(asset_clip_prim, 'startTime')
        endTime =  get_timecode(asset_clip_prim, 'endTime')

        playStart = get_timecode(asset_clip_prim, 'playStart')
        playEnd = get_timecode(asset_clip_prim, 'playEnd')

        source_range = otime.TimeRange.range_from_start_end_time_inclusive(
            otime.RationalTime(startTime, self.fps),
            otime.RationalTime(endTime, self.fps))

        clip = otio.schema.Clip()
        clip.source_range = source_range

        for usd_prim in asset_clip_prim.GetChildren():
            usd_type = usd_prim.GetTypeName()
            usd_path = usd_prim.GetPath()
            self.process_asset(stage, usd_path, usd_prim)
        
        self.tracks[-1].append(clip)
        pass
                    
    def recurse_track(self, stage, track_path, track_prim):
        track_usd_type = track_prim.GetAttribute('trackType').Get()

        if track_usd_type != 'Audio' and track_usd_type != 'Video':
            return

        track_type = track_usd_type

        print(f'Processing track {track_type}')
        
        name = track_prim.GetAttribute('label').Get()
        track = otio.schema.Track(name, None, None, track_type)
        self.tracks.append(track)

        
        for usd_prim in track_prim.GetAllChildren():
            usd_path  = usd_prim.GetPath()
            prim_type = usd_prim.GetTypeName()
            if prim_type == 'AssetClip':
                self.process_asset_clip(stage, usd_path, usd_prim)

    def recurse_sequence(self, stage, sequence_prim):
        self.timeline = otio.schema.Timeline()

        self.usd_sequence = sequence_prim

        #
        # Get global timing information for Sequence
        #
        self.startTimecode = stage.GetStartTimeCode()
        self.endTimecode = stage.GetEndTimeCode()
        self.fps         = stage.GetTimeCodesPerSecond()
        
        for usd_prim in sequence_prim.GetAllChildren():
            usd_path  = usd_prim.GetPath()
            prim_type = usd_prim.GetTypeName()
            if prim_type == 'Track':
                self.recurse_track(stage, usd_path, usd_prim)

        stack = otio.schema.Stack()
        for track in self.tracks:
            stack.append(track)
        self.timeline.tracks = stack
        pass
    
    def run(self):
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
        usd_path = self.path
        usd_prim = stage.GetPrimAtPath(usd_path)
        if not usd_prim:
            print(f'''USD path "{usd_path}" is invalid Sequence primitive!

Use -p <path> for passing the path to a new
path or an already existing Sequence primitive.

Valid Sequence primitives in stage:''')
            found = False
            for x in stage.Traverse():
                if x.GetTypeName() == 'Sequence':
                    print(f'\t{x} is a Sequence primitive.')
                    found = True
            if not found:
                print('\tNone')
            exit(1)
            
        
        if usd_prim: 
            prim_type = usd_prim.GetTypeName()
            if prim_type !=  'Sequence':
                print(f'''USD path "{usd_path}" already has a primitive, 
of type {prim_type}!

Use -p <path> for passing the path to a new
path or an already existing Sequence primitive.

Valid Sequence primitives in stage:''')
                found = False
                for x in stage.Traverse():
                    if x.GetTypeName() == 'Sequence':
                        print(f'\t{x} is a Sequence primitive.')
                        found = True
                if not found:
                    print('\tNone')
                exit(1)

        
        self.recurse_sequence(stage, usd_prim)
                
        #
        # Export modified stage to output file
        #
        if self.output_file == self.usd_file:
            if Options.log_level >= LogLevel.NORMAL:
                print('WARNING: Saving over original USD file.')
                Options.continue_prompt()
        else:
            #
            # Check if otio file already exists
            #
            if os.path.isfile(self.output_file):
                if Options.log_level >= LogLevel.NORMAL:
                    print(f'"{self.output_file}" already exists!  '
                          'Will overwrite it.')
                    Options.continue_prompt()
                

        stage.Export(self.output_file, addSourceFileComment=self.comment)
        if Options.log_level >= LogLevel.NORMAL:
            print(f'Saved "{self.output_file}".')
