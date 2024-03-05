

from usdOtio.options import Options, Verbose
from usdOtio.time_range import TimeRange

class TimeRangeMixin:
    def _set_time_range(self, stage, usd_path, name):
        s = self.jsonData.get(name)
        range_prim = None
        if s:
            range_path = usd_path + f'/{name}'
            range_prim = TimeRange(s)
            range_prim.to_usd(stage, range_path)
            if Options.verbose == Verbose.DEBUG:
                print(f'\t\tCreated time range at {range_path}')

        return range_prim
    
    def _create_time_range(self, usd_prim):
        time_range = TimeRange()
        return time_range.from_usd(usd_prim)
