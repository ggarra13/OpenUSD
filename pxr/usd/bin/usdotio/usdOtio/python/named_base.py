
import json

from usdOtio.base       import Base
from usdOtio.options    import Options, Verbose

class NamedBase(Base):

    FILTER_KEYS = [
        'metadata',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.metadata = json.dumps(self.jsonData.get('metadata', '{}'))
        if otio_item:
            self.name = otio_item.name
        else:
            self.name = self.__class__.__name__

    def from_usd(self, usd_prim):
        return super().from_usd(usd_prim)
    
    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(NamedBase.FILTER_KEYS)

    def _set_attributes(self, usd_prim):
        self._set_attribute(usd_prim, 'metadata', self.metadata)
        
        super()._set_attributes(usd_prim)

    def _get_attributes(self, usd_prim):
        super()._get_attributes(usd_prim)

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
