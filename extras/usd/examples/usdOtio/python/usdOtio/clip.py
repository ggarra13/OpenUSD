
import json

from usdOtio.base import Base

class Clip(Base):
    def __init__(self, otio_item = None):
        self.effects = []
        super().__init__(otio_item)

    def append_effect(self, effect):
        self.effects.append(effect)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove effects
        self.jsonData.pop('effects')

    def from_usd(self):
        json_strings = [child.to_json_string() for child in self.effects]
        self.jsonData['effects'] = json_strings
        return to_json_string()
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioClip')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim

