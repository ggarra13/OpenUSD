
import json

from usdOtio.named_base  import NamedBase
from usdOtio.rational_time import RationalTime
from usdOtio.track import Track

class Stack(NamedBase):

    FILTER_KEYS = ['effects',
                   'markers',
                   'children',
                   'source_range',
                   ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.children = []
        self.effects = []
        self.markers = []
        if not otio_item:
            self.jsonData = {
                'OTIO_SCHEMA' : 'Stack.1',
                'name'     : 'Stack',
                'metadata' : {},
                'source_range' : None,
                'effects' : [],
                'markers' : [],
                'enabled' : True,
            }

    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(Stack.FILTER_KEYS)
        
    def append_effect(self, effect):
        self.effects.append(effect)
        
    def append_marker(self, marker):
        self.markers.append(marker)

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)

    def from_usd(self, usd_prim):

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            usd_child_prim = None
            if usd_type == 'OtioTrack':
                usd_child_prim = Track()
            elif usd_type == 'OtioStack':
                usd_child_prim = Stack()
            elif usd_type == 'OtioRationalTime':
                usd_child_prim = RationalTime()
            elif usd_type == 'OtioMarker':
                marker_prim = Marker()
                marker_prim.from_usd(x)
                self.append_marker(marker_prim)
            elif usd_type == 'OtioEffect':
                effect_prim = Effect()
                effect_prim.from_usd(x)
                self.append_effect(effect_prim)
            elif usd_type == 'OtioTimeRange':
                range_prim = TimeRange()
                self.jsonData[usd_name] = range_prim.from_usd(x)
            else:
                print(f'WARNING: Unknown primitive {x} type {usd_type}')

            if usd_child_prim:
                usd_child_prim.from_usd(x)
                self.append_child(usd_child_prim)
            
        json_strings = [json.loads(x.to_json_string()) for x in self.effects]
        self.jsonData['effects'] = json_strings
        
        json_strings = [json.loads(x.to_json_string()) for x in self.markers]
        self.jsonData['markers'] = json_strings
        
        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings
        
        return self.jsonData

    def to_usd(self, stage, usd_path):
        super()._set_time_range(stage, usd_path, 'source_range')
        usd_prim = self.create_usd(stage, usd_path, 'OtioStack')
        
        s = self.jsonData.get('source_range')
        if s:
            source_range_path = usd_path + '/source_range'
            source_range_prim = TimeRange(s)
            source_range_prim.to_usd(stage, source_range_path)
            self.source_range = source_range_prim
        
        return usd_prim
