# Copyright 2024 Gonzalo Garramuño for Signly
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
#


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
