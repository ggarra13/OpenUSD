
import json

from usdOtio.base import Base
from usdOtio.v2d import V2d

class Box2d(Base):

    FILTER_KEYS = [
        'min',
        'max',
    ]
    
    def __init__(self, jsonData = {}):
        self.jsonData = jsonData.copy() # must copy the json data!

    def to_json_string(self):
        return self.jsonData

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Box2D.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        for x in usd_prim.GetChildren():
            usd_name = x.GetName()
            usd_type = x.GetTypeName()
            if usd_type == 'OtioV2d':
                time = RationalTime()
                self.jsonData[usd_name] = time.from_usd(x)
            else:
                print(f'WARNING: (box2d.py) Unknown node {usd_type} for '
                      f'{usd_prim}')

        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioBox2d')
        
        vmin = V2d(self.jsonData['min'])
        vmin_path = usd_path + '/min'
        vmin_prim = vmin.to_usd(stage, vmin_path)
        
        vmax = V2d(self.jsonData['max'])
        vmax_path = usd_path + '/max'
        vmax_prim = vmax.to_usd(stage, vmax_path)
        
        return usd_prim

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Box2d.FILTER_KEYS)
