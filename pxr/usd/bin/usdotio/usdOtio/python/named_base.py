
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
