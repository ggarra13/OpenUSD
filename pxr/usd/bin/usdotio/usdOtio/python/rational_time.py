
import json

from usdOtio.base import Base

class RationalTime(Base):
    
    def __init__(self, json_data = None):
        if json_data:
            self.jsonData = json_data.copy()
        else:
            self.jsonData = {
                'value' : 0,
                'rate'  : 24
            }
        
    def from_usd(self, usd_prim):
        self._get_attributes(usd_prim)
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        usd_prim = super()._create_usd(stage, usd_path, 'OtioRationalTime')
        return usd_prim
    
    def _set_attributes(self, usd_prim):   
        attr = usd_prim.GetAttribute('value')
        attr.Set(self.jsonData['value'])
        
        attr = usd_prim.GetAttribute('rate')
        attr.Set(self.jsonData['rate'])

        super()._set_attributes(usd_prim)
