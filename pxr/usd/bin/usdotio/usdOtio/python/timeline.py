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
from usdOtio.options import Options
from usdOtio.rational_time_mixin import RationalTimeMixin
from usdOtio.stack import Stack
from usdOtio.track import Track

class Timeline(NamedBase, RationalTimeMixin):

    FILTER_KEYS = [
        'global_start_time',
        'tracks',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.stack = {}
        self.global_start_time = None
        if otio_item:
            self.global_start_time = self.jsonData['global_start_time']
            
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Timeline.FILTER_KEYS)
    
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)

        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            if usd_type == 'OtioStack':
                stack_prim = Stack()
                self.jsonData['tracks'] = stack_prim.from_usd(x)
            elif usd_type == 'OtioRationalTime': 
                self.jsonData['global_start_time'] = \
                    self._create_rational_time(x)
                continue
            else:
                print(f'WARNING: (timeline.py) Unknown node attached to {usd_prim}!')
                continue

        return self.to_json_string()
    
    def to_usd(self, stage, usd_path):
        self._set_rational_time(stage, usd_path, 'global_start_time')
        
        usd_prim = self._create_usd(stage, usd_path, 'OtioTimeline')

        return usd_prim


    def _set_usd_attributes(self, usd_prim):
        #
        # Check if data is not empty
        #
        prim_type = usd_prim.GetTypeName()
        attr = usd_prim.GetAttribute('OTIO_SCHEMA')
        old_data = attr.Get()
        if old_data and old_data != '':
            print(f'\n\nWARNING: json data for {self.item_otio} is not empty:')
            print(f'{old_data[:256]}...')
            Options.continue_prompt()

        super()._set_usd_attributes(usd_prim)

        
