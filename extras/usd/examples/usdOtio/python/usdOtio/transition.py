
from usdOtio.base import Base

class Transition(Base):
    
    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTransition')
        if self.verbose:
            print(f'Created Transition at {usd_path}')
        self._store_json_string(usd_path, usd_prim)
        return usd_prim


