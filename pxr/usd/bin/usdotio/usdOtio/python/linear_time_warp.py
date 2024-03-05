
from usdOtio.effect import Effect

class LinearTimeWarp(Effect):
        
    def to_usd(self, stage, usd_path):
        usd_prim = self._create_usd(stage, usd_path, 'OtioLinearTimeWarp')
        return usd_prim
        
