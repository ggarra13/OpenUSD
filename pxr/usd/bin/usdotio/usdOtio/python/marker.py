
import json

from usdOtio.named_base import NamedBase

class Marker(NamedBase):
    
    FILTER_KEYS = [
        'marked_range',
    ]

    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            usd_name = x.GetName()
            if usd_type == 'OtioTimeRange':
                self.jsonData[usd_name] = self._create_time_range(x)
            else:
                print(f'WARNING: (marker.py) Unknown node {usd_type}' \
                      f'attached to {usd_prim}!')
                continue
        
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        if self.otio_item.marked_range:
            marker_path = usd_path + '/marked_range'
            marker_prim = TimeRange(self.jsonData['marked_range'])
            marker_prim.to_usd(stage, marker_path)
            
        usd_prim = self._create_usd(stage, usd_path, 'OtioMarker')
        return usd_prim
        
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Marker.FILTER_KEYS)
