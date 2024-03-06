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

from usdOtio.base       import Base
from usdOtio.options    import Options, Verbose

class NamedBase(Base):

    FILTER_KEYS = [
        'metadata',
    ]
    
    def __init__(self, otio_item = None):
        """Constructor.
        This abstract class handles all classes that have a name and a
        metadata.

        Args:
        otio_item (type): Optional otio.schema.* type

        """

        super().__init__(otio_item)
        self.metadata = json.dumps(self.jsonData.get('metadata', '{}'))
        if otio_item:
            self.name = otio_item.name
        else:
            self.name = self.__class__.__name__

    def _filter_keys(self):
        """Filter the attributes for this abstract class and its children
        classes.
        """

        super()._filter_keys()
        self._remove_keys(NamedBase.FILTER_KEYS)

    def _set_usd_attributes(self, usd_prim):
        """Sets the attributes for this abstract class and its

        Args:
        arg1 (type): Description of arg1

        Returns:
        return_type: Description of the return value

        Raises:
        Exception: Description of when this exception can be raised

        """

        self._set_usd_attribute(usd_prim, 'metadata', self.metadata)
        
        super()._set_usd_attributes(usd_prim)

    def _get_usd_attributes(self, usd_prim):
        super()._get_usd_attributes(usd_prim)

        # Convert the metadata string into an actual dict
        metadata = self.jsonData.get('metadata')
        if metadata:
            try:
                self.jsonData['metadata'] = json.loads(metadata)
            except json.JSONDecodeError as e:
                # Handle the error if JSON decoding fails
                print(f"Error decoding JSON: {e}")
        else:
            self.jsonData['metadata'] = {}
