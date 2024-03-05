

from usdOtio.named_base import NamedBase
from usdOtio.rational_time_mixin import RationalTimeMixin

class Transition(NamedBase, RationalTimeMixin):

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
        
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Transition.FILTER_KEYS)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        for x in usd_prim.GetChildren():
            usd_name = x.GetName()
            usd_type = x.GetTypeName()
            if usd_type == 'OtioRationalTime':
                self.jsonData[usd_name] = self._create_rational_time(x)
            else:
                print(f'WARNING: (transition.py) Unknown node {usd_type} for '
                      f'{usd_prim}')
        
        return self.jsonData
    
    def to_usd(self, stage, usd_path):
        self._set_rational_time(stage, usd_path, 'in_offset')
        self._set_rational_time(stage, usd_path, 'out_offset')
        
        usd_prim = self._create_usd(stage, usd_path, 'OtioTransition')
        return usd_prim
