#
# Normal python imports
#
import sys

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
from usdOtio.track import Track
from usdOtio.effect import Effect
from usdOtio.linear_time_warp import LinearTimeWarp

    
class UsdOtioAdd:
    def __init__(self, usd_file, otio_file, output_file, path = '/',
                 comment = True):
        self.usd_file = usd_file
        self.otio_file = otio_file
        self.output_file = output_file
        self.path = path
        self.comment = not comment

    def create_effect(self, stage, usd_path, effect):
        if isinstance(effect, otio.schema.LinearTimeWarp):
            usd_path = usd_path + f'/LinearTimeWarp_{self.effect_index}'
            usd_effect_item = LinearTimeWarp(effect)
        else:
            usd_path = usd_path + f'/Effect_{self.effect_index}'
            usd_effect_item = Effect(effect)
            
        usd_effect_item.to_usd(stage, usd_path)
        
    @staticmethod
    def get_first_stack(timeline):
        return None

    def parse_effects(self, stage, usd_path, effects):
        for effect in effects:
            self.create_effect(stage, usd_path, effect)
            self.effect_index += 1
    
    def run(self):
        """
        Run the otio add algorithm.
        """

        #
        # Open the original scene file
        # 
        stage = Usd.Stage.Open(self.usd_file)
                
        #
        # Try to validate the otio file
        #
        try:
            timeline = otio.adapters.read_from_file(self.otio_file)
        except ValueError as e:
            if self.otio_file.endswith('.otio'):
                print(f'ERROR: Corrupt .otio file "{self.otio_file}: {e}"!',
                      file=sys.stderr)
            else:
                print(f'ERROR: Could not convert "{self.otio_file}" with '
                      'any adapter!', file=sys.stderr)
            exit(1)
            
        #
        # Create an USD otio primitive at path/otio.
        #
        usd_path = self.path
        usd_prim = stage.GetPrimAtPath(usd_path)
        if usd_prim: 
            prim_type = usd_prim.GetTypeName()
            if prim_type != 'OtioTimeline':
                print(f'''USD path "{usd_path}" already has a primitive, 
of type {prim_type}!

Use -p <path> for passing the path to a new
path or an already existing OtioTimeline primitive.

Valid OtioTimeline primitives in stage:''')
                found = False
                for x in stage.Traverse():
                    if x.GetTypeName() == 'OtioTimeline':
                        print(f'\t{x} is an OtioTimeline primitive.')
                        found = True
                if not found:
                    print('\tNone')
                exit(1)
        
        usd_otio_item = Timeline(timeline)
        usd_otio_item.to_usd(stage, usd_path)

        # Check if there's a stacks attribute (this is broken in Python)
        stack = None
        stack_path = usd_path + '/Stack'
        
        stack = timeline.tracks
        if stack:
            usd_stack_item = Stack(stack)
        else:
            usd_stack_item = Stack(otio.schema.Stack())
            
        usd_stack_item.to_usd(stage, stack_path)
            
  
        

        track_index = 1
        video_track_index = 1
        audio_track_index = 1
        self.effect_index = 1
        for track in timeline.tracks:
            if track.kind == 'Video':
                track_path = stack_path + f'/Video_{video_track_index}'
                video_track_index += 1
            elif track.kind == 'Audio':
                track_path = stack_path + f'/Audio_{audio_track_index}'
                audio_track_index += 1
            else:
                track_path = stack_path + f'/Track_{track_index}'
                track_index += 1
            usd_track_item = Track(track)
            usd_track_item.to_usd(stage, track_path)
            
            usd_stack_item.append_child(usd_track_item)
        
            gap_index = 1
            clip_index = 1
            stack_index = 1
            transition_index = 1

            for child in track:

                usd_child_item = None
                usd_path = None
                can_have_effects = False
                
                if isinstance(child, otio.schema.Clip):
                    usd_path = track_path + f'/Clip_{clip_index}'
                    usd_child_item = Clip(child)
                    can_have_effects = True
                    clip_index += 1
                elif isinstance(child, otio.schema.Transition):
                    usd_path = track_path + f'/Transition_{transition_index}'
                    usd_child_item = Transition(child)
                    transition_index += 1
                elif isinstance(child, otio.schema.Gap):
                    usd_path = track_path + f'/Gap_{gap_index}'
                    usd_child_item = Gap(child)
                    can_have_effects = True
                    gap_index += 1
                elif isinstance(child, otio.schema.Stack):
                    usd_path = track_path + f'/Stack_{stack_index}'
                    usd_child_item = Stack(child)
                    can_have_effects = True
                    stack_index += 1
                else:
                    print('WARNING: Unknown child {child}')

                if usd_child_item:
                    usd_child_item.to_usd(stage, usd_path)

                    if can_have_effects:
                        self.parse_effects(stage, usd_path, child.effects)

            if track.effects:
                self.parse_effects(stage, usd_path, track.effects)
        
        #
        # Export modified stage to output file
        #
        if self.output_file == self.usd_file:
            print('WARNING: Overwriting USD file.')
            Options.continue_prompt()

        stage.Export(self.output_file, addSourceFileComment=self.comment)
