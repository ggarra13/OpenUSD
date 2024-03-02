
import json

from usdOtio.base import Base

class Item(Base):
    def __init__(self, otio_item = None):
        self.effects = []
        super().__init__(otio_item)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove effects
        self.jsonData.pop('effects')

    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        json_strings = [json.loads(child.to_json_string()) for child in self.effects]
        self.jsonData['effects'] = json_strings
        return self.to_json_string()
