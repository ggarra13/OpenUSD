
import json

from usdOtio.base import Base
from usdOtio.clip import Clip
from usdOtio.gap import Gap
from usdOtio.transition import Transition
from usdOtio.effect import Effect


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
        # Remove children and effects
        self.jsonData.pop('children')
        self.jsonData.pop('effects')
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            if usd_type == 'OtioClip':
                usd_prim = Clip()
                usd_prim.from_usd(x)
                self.children.append(usd_prim)
            elif usd_type == 'OtioGap':
                usd_prim = Gap()
                usd_prim.from_usd(x)
                self.children.append(usd_prim)
            elif usd_type == 'OtioTransition':
                usd_prim = Transition()
                usd_prim.from_usd(x)
                self.children.append(usd_prim)
            elif usd_type == 'OtioEffect':
                usd_prim = Effect()
                usd_prim.from_usd(x)
                self.effects.append(usd_prim)
                
        json_strings = [json.loads(child.to_json_string()) for child in self.children]
        self.jsonData['children'] = json_strings
        
        json_strings = [json.loads(effect.to_json_string()) for effect in self.effects]
        self.jsonData['effects'] = json_strings
        return self.to_json_string()

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTrack')
        self._store_json_string(usd_path, usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim
