
import json

from usdOtio.base import Base


class Track(Base):
    def __init__(self, otio_item = None):
        self.children = []
        self.effects = []
        super().__init__(otio_item)

    def append_child(self, child):
        self.children.append(child)
        
    def append_effect(self, effect):
        self.effects.append(effect)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        print('Called track.from_json_string()')
        # Remove children and effects
        self.jsonData.pop('children')
        self.jsonData.pop('effects')

    def from_usd(self):
        json_strings = [child.to_json_string() for child in self.children]
        self.jsonData['children'] = json_strings
        
        json_strings = [effect.to_json_string() for effect in self.effects]
        self.jsonData['effects'] = json_strings

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTrack')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim
