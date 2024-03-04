
import json

from usdOtio.media_reference import MediaReference

class MissingReference(MediaReference):
    
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, path)
        usd_prim = self.create_usd(stage, usd_path, 'OtioMissingReference')
        return usd_prim
