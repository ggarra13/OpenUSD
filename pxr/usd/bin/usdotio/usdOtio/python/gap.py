
import json

from usdOtio.item import Item

class Gap(Item):
    
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        usd_prim = self._create_usd(stage, usd_path, 'OtioGap')
        return usd_prim
