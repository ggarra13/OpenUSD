
import json

from usdOtio.base import Base
from usdOtio.stack import Stack
from usdOtio.track import Track

class Timeline(Base):
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.stack = {}

    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove children from jsonData
        self.jsonData.pop('tracks')
    
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            if usd_type == 'OtioStack':
                stack_prim = Stack()
                stack_prim.from_usd(x)
                self.stack = stack_prim

        stack = json.loads(self.stack.from_usd(usd_prim))
        self.jsonData['tracks'] = stack
        return self.to_json_string()
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTimeline')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim
