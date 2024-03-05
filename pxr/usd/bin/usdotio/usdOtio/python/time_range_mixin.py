

from usdOtio.options import Options, Verbose
from usdOtio.time_range import TimeRange

class TimeRangeMixin:
    def _set_time_range(self, stage, usd_path, name):
        range_prim = None
        json_data = self.jsonData.get(name)
        if json_data:
            range_path = usd_path + f'/{name}'
            range_prim = TimeRange(json_data)
            range_prim.to_usd(stage, range_path)
            if Options.verbose == Verbose.DEBUG:
                print(f'\t\tCreated time range at {range_path}')

        return range_prim
    
    def _create_time_range(self, usd_prim):
        time_range = TimeRange()
        return time_range.from_usd(usd_prim)
