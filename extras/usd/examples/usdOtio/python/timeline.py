
import json

from usdOtio.named_base import NamedBase
from usdOtio.options import Options
from usdOtio.rational_time import RationalTime
from usdOtio.stack import Stack
from usdOtio.track import Track

class Timeline(NamedBase):

    FILTER_KEYS = [
        'global_start_time',
        'tracks',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.stack = {}
        self.global_start_time = None
        if otio_item:
            self.global_start_time = self.jsonData['global_start_time']
            
    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(Timeline.FILTER_KEYS)
    
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            if usd_type == 'OtioStack':
                stack_prim = Stack()
                self.jsonData['tracks'] = stack_prim.from_usd(x)
            elif usd_type == 'OtioRationalTime':  
                time_prim = RationalTime()
                self.jsonData['global_start_time'] = time_prim.from_usd(x)
                continue
            else:
                print(f'WARNING: (timeline.py) Unknown node attached to {usd_prim}!')
                continue

        return self.to_json_string()
    
    def to_usd(self, stage, usd_path):
        usd_prim = self.create_usd(stage, usd_path, 'OtioTimeline')

        if self.global_start_time:
            start_path = usd_path + '/global_start_time'
            start_prim = RationalTime(self.global_start_time)
            start_prim.to_usd(stage, start_path)

        return usd_prim


    def _set_attributes(self, usd_prim):
        #
        # Check if data is not empty
        #
        prim_type = usd_prim.GetTypeName()
        attr = usd_prim.GetAttribute('OTIO_SCHEMA')
        old_data = attr.Get()
        if old_data and old_data != '':
            print(f'\n\nWARNING: json data for {self.item_otio} is not empty:')
            print(f'{old_data[:256]}...')
            Options.continue_prompt()

        super()._set_attributes(usd_prim)

        
