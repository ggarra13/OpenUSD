
import json

from usdOtio.media_reference import MediaReference

class ExternalReference(MediaReference):
    
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        usd_prim = self._create_usd(stage, usd_path, 'OtioExternalReference')
        return usd_prim

