
from usdOtio import Base

class Effect(usdOtio.Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioEffect')
        return usd_prim

