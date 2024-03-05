
from usdOtio.named_base import NamedBase

class Effect(NamedBase):
    def to_usd(self, stage, usd_path):
        usd_prim = self._create_usd(stage, usd_path, 'OtioEffect')
        return usd_prim
