
import json

from usdOtio.named_base import NamedBase
from usdOtio.time_range import TimeRange

class Marker(NamedBase):
    
    FILTER_KEYS = [
        'marked_range',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)

    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            usd_name = x.GetName()
            if usd_type == 'OtioTimeRange':  
                range_prim = TimeRange()
                self.jsonData[usd_name] = range_prim.from_usd(x)
            else:
                print(f'WARNING: (media_reference.py) Unknown node {usd_type} attached to {usd_prim}!')
                continue
        
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        if self.otio_item.marked_range:
            marker_path = usd_path + '/marked_range'
            marker_prim = TimeRange(self.jsonData['marked_range'])
            marker_prim.to_usd(stage, marker_path)
            
        usd_prim = self.create_usd(stage, usd_path, 'OtioMarker')
        return usd_prim
        
    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(Marker.FILTER_KEYS)
