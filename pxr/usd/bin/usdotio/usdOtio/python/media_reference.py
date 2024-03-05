
import json

from usdOtio.named_base import NamedBase
from usdOtio.time_range import TimeRange

class MediaReference(NamedBase):

    FILTER_KEYS = [
        'available_image_bounds',
        'available_range',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.available_image_bounds = \
            self.jsonData.get('available_image_bounds')

    def to_usd(self, stage, usd_path):
        self._set_time_range(stage, usd_path, 'available_range')
        super().to_usd(stage, usd_path)
        
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
        
    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(MediaReference.FILTER_KEYS)
