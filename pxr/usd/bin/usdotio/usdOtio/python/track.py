
import json, importlib

from usdOtio.clip import Clip
from usdOtio.effect import Effect
from usdOtio.item import Item
from usdOtio.gap import Gap
from usdOtio.marker import Marker
from usdOtio.transition import Transition
from usdOtio.time_range_mixin import TimeRangeMixin


class Track(Item, TimeRangeMixin):

    FILTER_KEYS = [
        'children',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.children = []
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            child_prim = None
            usd_name = x.GetName()
            print(f'Processing {usd_name}')
            if usd_type == 'OtioClip':
                child_prim = Clip()
            elif usd_type == 'OtioGap':
                child_prim = Gap()
            elif usd_type == 'OtioTransition':
                child_prim = Transition()
            elif usd_type == 'OtioStack':
                child_prim = self._create_stack(x)
            else:
                pass

            if child_prim:
                child_prim.from_usd(x)
                self.children.append(child_prim)
                print(f'children size={len(self.children)}')

        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings

        return self.jsonData

    def to_usd(self, stage, usd_path):
        self._set_time_range(stage, usd_path, 'source_range')
            
        usd_prim = self._create_usd(stage, usd_path, 'OtioTrack')
        
        return usd_prim

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Track.FILTER_KEYS)

    def _create_stack(self, x = None):
        #
        # We need to use importlib to avoid cyclic dependencies
        #
        stack_module = importlib.import_module("usdOtio.stack")
        stack = stack_module.Stack()
        return stack
