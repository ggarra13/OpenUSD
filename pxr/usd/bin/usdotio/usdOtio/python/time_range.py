
import json

from usdOtio.base import Base
from usdOtio.rational_time_mixin import RationalTimeMixin

class TimeRange(Base, RationalTimeMixin):

    FILTER_KEYS = [
        'start_time',
        'duration'
    ]
    
    def __init__(self, jsonData = {}):
        self.jsonData = jsonData.copy() # must copy the json data!
        self.otio_item  = None

    def to_json_string(self):
        return self.jsonData

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(TimeRange.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        for child_prim in usd_prim.GetChildren():
            usd_name = child_prim.GetName()
            usd_type = child_prim.GetTypeName()
            if usd_type == 'OtioRationalTime':
                self.jsonData[usd_name] = self._create_rational_time(child_prim)
            else:
                print(f'WARNING: (time_range.py) Unknown node {usd_type} for '
                      f'{usd_prim}')

        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        self._set_rational_time(stage, usd_path, 'start_time')
        self._set_rational_time(stage, usd_path, 'duration')
        
        usd_prim = self._create_usd(stage, usd_path, 'OtioTimeRange')
        
        
        return usd_prim
