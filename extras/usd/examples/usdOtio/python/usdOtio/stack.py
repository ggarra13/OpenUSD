
import json

from usdOtio.base  import Base
from usdOtio.track import Track

class Stack(Base):
    def __init__(self, otio_item = None):
        self.children = []
        super().__init__(otio_item)
        if not otio_item:
            self.jsonData = {
                'OTIO_SCHEMA' : 'Stack.1',
                'metadata' : {},
                'name' : '',
                'source_range' : None,
                'effects' : [],
                'markers' : [],
                'enabled' : True,
            }
            

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove children from jsonData
        self.jsonData.pop('children')

    def from_usd(self, usd_prim):
        usd_type = usd_prim.GetTypeName()
        if usd_type == 'OtioStack':
            self._extract_json_string(usd_prim)
        else:
            self.jsonData = {
                'OTIO_SCHEMA' : 'Stack.1',
                'metadata' : {},
                'name' : '',
                'source_range' : None,
                'effects' : [],
                'markers' : [],
                'enabled' : True,
            }

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            if usd_type == 'OtioTrack':
                track_prim = Track()
                track_prim.from_usd(x)
                self.append_child(track_prim)
            else:
                print(f'WARNING: Unknown primitive {x}')
                
        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings
        return self.to_json_string()

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioStack')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim
