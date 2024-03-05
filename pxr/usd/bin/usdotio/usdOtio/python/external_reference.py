
import json

from usdOtio.media_reference import MediaReference

class ExternalReference(MediaReference):
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        if otio_item:
            self.target_url = otio_item.target_url
    
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        usd_prim = self.create_usd(stage, usd_path, 'OtioExternalReference')
        return usd_prim

    def _set_attributes(self, usd_prim):
        self._set_attribute(usd_prim, 'target_url', self.target_url)
        
        super()._set_attributes(usd_prim)

