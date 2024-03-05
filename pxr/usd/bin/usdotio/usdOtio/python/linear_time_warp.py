
from usdOtio.effect import Effect

class LinearTimeWarp(Effect):
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        
    def to_usd(self, stage, usd_path):
        usd_prim = self.create_usd(stage, usd_path, 'OtioLinearTimeWarp')
        return usd_prim
        
