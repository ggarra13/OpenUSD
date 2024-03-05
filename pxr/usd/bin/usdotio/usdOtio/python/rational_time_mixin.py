

from usdOtio.options import Options, Verbose
from usdOtio.rational_time import RationalTime

class RationalTimeMixin:
    def _create_rational_time(self, usd_prim):
        rational_time = RationalTime()
        return rational_time.from_usd(usd_prim)

    def _set_rational_time(self, stage, usd_path, name):
        s = self.jsonData.get(name)

        time_prim = None
        if s:
            time_path = usd_path + f'/{name}'
            time_prim = RationalTime(s)
            time_prim.to_usd(stage, time_path)

        return time_prim
