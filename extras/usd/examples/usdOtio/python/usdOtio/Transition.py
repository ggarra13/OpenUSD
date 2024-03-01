
from usdOtio import Base

class Transition(usdOtio.Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTransition')
        return usd_prim


