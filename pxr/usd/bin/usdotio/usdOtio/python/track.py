
import json, importlib

from usdOtio.clip import Clip
from usdOtio.effect import Effect
from usdOtio.item import Item
from usdOtio.gap import Gap
from usdOtio.marker import Marker
from usdOtio.transition import Transition


class Track(Item):

    FILTER_KEYS = [
        'children',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.children = []
        if otio_item:
            self.enabled = otio_item.enabled
            self.kind = otio_item.kind
                
    def create_stack(x = None):
        stack_module = importlib.import_module("usdOtio.stack")
        stack = stack_module.Stack(x)
        return stack
        
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
            if usd_type == 'OtioClip':
                child_prim = Clip()
                self.children.append(child_prim)
            elif usd_type == 'OtioGap':
                child_prim = Gap()
                self.children.append(child_prim)
            elif usd_type == 'OtioTransition':
                child_prim = Transition()
                self.children.append(child_prim)
            elif usd_type == 'OtioStack':
                child_prim = create_stack()
                self.children.append(child_prim)
            else:
                pass

            if child_prim:
                child_prim.from_usd(x)

        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings

        return self.jsonData

    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
            
        if self.otio_item.source_range:
            source_range_path = usd_path + '/source_range'
            source_range_prim = TimeRange(self.jsonData['source_range'])
            source_range_prim.to_usd(stage, source_range_path)
            self.source_range = source_range_prim
            
        usd_prim = self.create_usd(stage, usd_path, 'OtioTrack')
        
        return usd_prim

    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(Track.FILTER_KEYS)

            
    def _set_attributes(self, usd_prim):
        super()._set_attributes(usd_prim)
        
        self._set_attribute(usd_prim, "enabled", self.enabled)
        self._set_attribute(usd_prim, "kind", self.kind)
