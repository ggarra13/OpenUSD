
from usdOtio import Base

class Clip(usdOtio.Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioClip')
        return usd_prim

