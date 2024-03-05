

from usdOtio.options import Options, Verbose
from usdOtio.box2d import Box2d

class Box2dMixin:
    def _set_box2d(self, stage, usd_path, name):
        box2d_prim = None
        json_data = self.jsonData.get(name)
        if json_data:
            box2d_path = usd_path + f'/{name}'
            box2d_prim = Box2d(json_data)
            box2d_prim.to_usd(stage, box2d_path)
            if Options.verbose == Verbose.DEBUG:
                print(f'\t\tCreated time box2d at {box2d_path}')

        return box2d_prim
    
    def _create_box2d(self, usd_prim):
        box2d = Box2d()
        return box2d.from_usd(usd_prim)
