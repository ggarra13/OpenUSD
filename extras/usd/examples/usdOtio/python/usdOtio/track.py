
from usdOtio.base import Base
import json

class Track(Base):
    def __init__(self, otio_item = None):
        self.children = []
        self.effects = []
        super().__init__(otio_item)

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove children and effects
        self.jsonData.pop('children')
        self.jsonData.pop('effects')

    def to_json_string(self):

        json_strings = [child.to_json_string() for child in self.children]
        self.jsonData['children'] = json_strings
        
        json_strings = [child.to_json_string() for child in self.effects]
        self.jsonData['effects'] = json_strings

        return json.dumps(self.jsonData)

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTrack')
        if self.verbose:
            print(f'Created Track at {usd_path}')
        self._store_json_string(usd_path, usd_prim)
        return usd_prim
