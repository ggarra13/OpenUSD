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

import json, importlib

from usdOtio.clip import Clip
from usdOtio.composition import Composition
from usdOtio.effect import Effect
from usdOtio.item import Item
from usdOtio.gap import Gap
from usdOtio.marker import Marker
from usdOtio.transition import Transition
from usdOtio.time_range_mixin import TimeRangeMixin


class Track(Composition):

    FILTER_KEYS = [
        'children',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.children = []
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_type = x.GetTypeName()
            child_prim = None
            usd_name = x.GetName()
            if usd_type == 'OtioClip':
                child_prim = Clip()
            elif usd_type == 'OtioGap':
                child_prim = Gap()
            elif usd_type == 'OtioTransition':
                child_prim = Transition()
            elif usd_type == 'OtioStack':
                child_prim = self._create_stack(x)
            else:
                pass

            if child_prim:
                child_prim.from_usd(x)
                self.children.append(child_prim)

        json_strings = [json.loads(x.to_json_string()) for x in self.children]
        self.jsonData['children'] = json_strings

        return self.jsonData

    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        
        usd_prim = self._create_usd(stage, usd_path, 'OtioTrack')
        return usd_prim

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Track.FILTER_KEYS)

    def _create_stack(self, x = None):
        #
        # We need to use importlib to avoid cyclic dependencies
        #
        stack_module = importlib.import_module("usdOtio.stack")
        stack = stack_module.Stack()
        return stack
