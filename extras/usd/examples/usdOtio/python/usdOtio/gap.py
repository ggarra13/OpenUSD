
import json

from usdOtio.item import Item

class Gap(Item):
    def __init__(self, otio_item = None):
        self.effects = []
        super().__init__(otio_item)

    def to_json_string(self, usd_prim):
        super().from_usd(usd_prim)
        json_strings = [child.to_json_string() for child in self.effects]
        self.jsonData['effects'] = json_strings
        return json.dumps(self.jsonData)
