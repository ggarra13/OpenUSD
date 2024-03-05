
import json

from usdOtio.base import Base

class V2d(Base):

    FILTER_KEYS = [
        'x',
        'y',
    ]
    
    def __init__(self, json_data = None):
        if json_data:
            self.jsonData = json_data.copy()
        else:
            self.jsonData = {
                'x' : 0,
                'y' : 0
            }
    
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(RationalTime.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioV2d')
        self._set_attributes(usd_prim)
        return usd_prim
    
    def _set_attributes(self, usd_prim):   
        attr = usd_prim.GetAttribute('x')
        attr.Set(self.jsonData['x'])
        
        attr = usd_prim.GetAttribute('y')
        attr.Set(self.jsonData['y'])
