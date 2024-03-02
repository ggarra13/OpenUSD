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
''')
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
''')
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
    
class UsdOtioAdd:
    def __init__(self, usd_file, otio_file, output_file, path = '/'):
        self.usd_file = usd_file
        self.otio_file = otio_file
        self.output_file = output_file
        self.path = path

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
        except:
            if self.otio_file.endswith('.otio'):
                print(f'ERROR: Corrupt .otio file "{self.otio_file}"!')
            else:
                print(f'ERROR: Could not convert "{self.otio_file}" with '
                      'any adapter!')
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
        

        # Check if there's a stacks attribute
        stack = None
        stack_path = usd_path + '/stack'
        if hasattr(timeline, "stacks"):
            # Access the first stack if it exists
            if timeline.stacks:
                print("Retrieved the first stack:", first_stack)
                stack = timeline.stacks[0]
                usd_stack_item = Stack(stack)
            else:
                usd_stack_item = Stack()
        else:
            usd_stack_item = Stack()
            
        usd_stack_item.to_usd(stage, stack_path)
            
  
        

        track_index = 0
        effect_index = 0
        for track in timeline.tracks:
            
            track_path = stack_path + f'/track_{track_index}'
            usd_track_item = Track(track)
            usd_track_item.to_usd(stage, track_path)
            
            usd_stack_item.append_child(usd_track_item)
            
            track_index += 1

            gap_index = 0
            clip_index = 0
            transition_index = 0

            for child in track:

                usd_otio_item = None
                usd_path = None
                can_have_effects = False

                if isinstance(child, otio.schema.Clip):
                    usd_path = track_path + f'/clip_{clip_index}'
                    usd_otio_item = Clip(child)
                    can_have_effects = True
                    clip_index += 1
                    # Do something with the Clip
                elif isinstance(child, otio.schema.Transition):
                    usd_path = track_path + f'/transition_{transition_index}'
                    usd_otio_item = Transition(child)
                    transition_index += 1
                elif isinstance(child, otio.schema.Gap):
                    usd_path = track_path + f'/gap_{gap_index}'
                    usd_otio_item = Gap(child)
                    can_have_effects = True
                    gap_index += 1
                else:
                    print('Not creating anything!')

                if usd_otio_item:
                    usd_otio_item.to_usd(stage, usd_path)

                    if can_have_effects:
                        for effect in child.effects:
                            usd_path = usd_path + f'/effect_{effect_index}'
                            usd_effect_item = Effect(effect)
                            usd_effect_item.to_usd(stage, usd_path)
                            usd_effect_item.from_json_string(effect.to_json_string())
                            usd_otio_item.append_effect(usd_effect_item)
                            
                            effect_index += 1

            if track.effects:
                for effect in track.effects:
                    usd_path = usd_path + f'/effect_{effect_index}'
                    usd_otio_item = Effect(child)
                    usd_effect_item.to_usd(stage, usd_path)
                
                    effect_index += 1
        
        #
        # Export modified stage to output file
        #
        if self.output_file == self.usd_file:
            print('WARNING: Overwriting USD file.')
            Options.continue_prompt()
        stage.Export(self.output_file)
