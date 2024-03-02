
import json

from usdOtio.item import Item

class Clip(Item):
    def __init__(self, otio_item = None):
        self.effects = []
        super().__init__(otio_item)
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioClip')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim

