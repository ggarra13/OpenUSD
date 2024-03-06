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

import opentimelineio as otio

from usdOtio.clip import Clip
from usdOtio.item import Item
from usdOtio.marker import Marker
from usdOtio.named_base  import NamedBase
from usdOtio.rational_time_mixin import RationalTimeMixin
from usdOtio.time_range_mixin import TimeRangeMixin
from usdOtio.track import Track

class Stack(Item, TimeRangeMixin, RationalTimeMixin):

    FILTER_KEYS = [
                   'children',
                   ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.children = []
        if not otio_item:
            self.jsonData = json.loads(otio.schema.Stack().to_json_string())
        
    def append_effect(self, effect):
        self.effects.append(effect)
        
    def append_marker(self, marker):
        self.markers.append(marker)

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)

    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            usd_name = x.GetName()
            child_prim = None
            if usd_type == 'OtioTrack':
                child_prim = Track()
            elif usd_type == 'OtioStack':
                child_prim = Stack()
            elif usd_type == 'OtioClip':
                child_prim = Clip()
            elif usd_type == 'OtioRationalTime':
                child_prim = RationalTime()
            elif usd_type == 'OtioMarker':
                marker_prim = Marker()
                marker_prim.from_usd(x)
                self.append_marker(marker_prim)
            elif usd_type == 'OtioEffect':
                effect_prim = Effect()
                effect_prim.from_usd(x)
                self.append_effect(effect_prim)
            elif usd_type == 'OtioTimeRange':
                range_prim = TimeRange()
                self.jsonData[usd_name] = range_prim.from_usd(x)
            else:
                print(f'WARNING: Unknown primitive {x} type {usd_type}')

            if child_prim:
                child_prim.from_usd(x)
                self.append_child(child_prim)
        
        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings
        
        return self.jsonData

    def to_usd(self, stage, usd_path):
        super()._set_time_range(stage, usd_path, 'source_range')
        usd_prim = self._create_usd(stage, usd_path, 'OtioStack')
        return usd_prim

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Stack.FILTER_KEYS)
