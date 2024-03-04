
import json

from usdOtio.base import Base
from usdOtio.rational_time import RationalTime

class TimeRange(Base):

    FILTER_KEYS = [
        'start_time',
        'duration',
    ]
    
    def __init__(self, jsonData = {}):
        self.jsonData = jsonData.copy() # must copy the json data!
        self.otio_item  = None
        self.start_time = None
        self.duration   = None

    def to_json_string(self):
        return self.jsonData

    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(TimeRange.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        for x in usd_prim.GetChildren():
            usd_name = x.GetName()
            usd_type = x.GetTypeName()
            if usd_type == 'OtioRationalTime':
                time = RationalTime()
                self.jsonData[usd_name] = time.from_usd(x)
            else:
                print(f'WARNING: (time_range.py) Unknown node {usd_type} for '
                      f'{usd_prim}')

        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTimeRange')
        
        start_time = RationalTime(self.jsonData['start_time'])
        start_path = usd_path + '/start_time'
        start_prim = start_time.to_usd(stage, start_path)
        
        duration = RationalTime(self.jsonData['duration'])
        duration_path = usd_path + '/duration'
        duration_prim = duration.to_usd(stage, duration_path)
        
        self._set_attributes(usd_prim)
        return usd_prim

    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(TimeRange.FILTER_KEYS)
