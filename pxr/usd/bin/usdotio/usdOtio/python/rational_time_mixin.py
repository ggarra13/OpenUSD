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


from usdOtio.options import Options, Verbose
from usdOtio.rational_time import RationalTime

class RationalTimeMixin:
    def _create_rational_time(self, usd_prim):
        rational_time = RationalTime()
        return rational_time.from_usd(usd_prim)

    def _set_rational_time(self, stage, usd_path, name):
        s = self.jsonData.get(name)

        time_prim = None
        if s:
            time_path = usd_path + f'/{name}'
            time_prim = RationalTime(s)
            time_prim.to_usd(stage, time_path)

        return time_prim
