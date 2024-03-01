
from usdOtio.base import Base

class Effect(Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioEffect')
        if self.verbose:
            print(f'Created Effect at {usd_path}')
        self._store_json_string(usd_path, usd_prim)
        return usd_prim

