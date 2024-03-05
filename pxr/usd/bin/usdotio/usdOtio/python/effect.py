
from usdOtio.named_base import NamedBase

class Effect(NamedBase):

    ATTRIBUTES = [
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)

    def filter_keys(self):
        super().filter_keys()
        
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        usd_prim = self.create_usd(stage, usd_path, 'OtioEffect')
        return usd_prim
