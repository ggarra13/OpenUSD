
from usdOtio.base import Base

class Clip(Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioClip')
        if self.verbose:
            print(f'Created Clip at {usd_path}')
        self._store_json_string(usd_path, usd_prim)
        return usd_prim

