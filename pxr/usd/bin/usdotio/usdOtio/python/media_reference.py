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

import json

from usdOtio.named_base import NamedBase
from usdOtio.time_range_mixin import TimeRangeMixin


class MediaReference(NamedBase, TimeRangeMixin):

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
                self.jsonData[usd_name] = self._create_time_range(x)
            else:
                print(f'WARNING: (media_reference.py) Unknown node {usd_type} attached to {usd_prim}!')
                continue
        
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(MediaReference.FILTER_KEYS)
