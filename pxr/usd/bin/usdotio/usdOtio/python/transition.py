

from usdOtio.named_base import NamedBase
from usdOtio.rational_time import RationalTime

class Transition(NamedBase):

    FILTER_KEYS = [
        'in_offset',
        'out_offset',
    ]

    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        if otio_item:
            self.transition_type = otio_item.transition_type
        else:
            self.transition_type = 'SMPTE_Dissolve'
        
    def filter_keys(self):
        super().filter_keys()
        self._filter_keys(Transition.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        for x in usd_prim.GetChildren():
            usd_name = x.GetName()
            usd_type = x.GetTypeName()
            if usd_type == 'OtioRationalTime':
                time = RationalTime()
                self.jsonData[usd_name] = time.from_usd(x)
            else:
                print(f'WARNING: (transition.py) Unknown node {usd_type} for '
                      f'{usd_prim}')

        
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        in_offset_path = usd_path + '/in_offset'
        in_offset_prim = RationalTime(self.jsonData['in_offset'])
        in_offset_prim.to_usd(stage, in_offset_path)
        
        out_offset_path = usd_path + '/out_offset'
        out_offset_prim = RationalTime(self.jsonData['out_offset'])
        out_offset_prim.to_usd(stage, out_offset_path)
        
        usd_prim = self.create_usd(stage, usd_path, 'OtioTransition')
        return usd_prim
