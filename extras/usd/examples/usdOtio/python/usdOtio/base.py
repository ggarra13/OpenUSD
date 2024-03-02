
import json

from usdOtio.options import Options

class Base:
    
    def __init__(self, otio_item = None):
        self.jsonData = {}
        if otio_item:
            self.from_json_string(otio_item.to_json_string())

    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        return json.dumps(self.jsonData)

    def from_usd(self, usd_prim):
        self._extract_json_string(usd_prim)
        return self.to_json_string()
    
    def to_usd(self, stage, usd_path):
        pass

    def _store_json_string(self, usd_path, usd_prim):
        #
        # Check if data is not empty
        #
        old_data = usd_prim.GetAttribute('jsonData').Get()
        if old_data and old_data != '':
            print(f'\n\nWarning jsonData for {usd_path} is not empty:')
            print(f'{old_data[:256]}...')
            Options.continue_prompt()
            
        #
        # Attach the json data to the otio primitive
        #
        usd_prim.GetAttribute('jsonData').Set(self.to_json_string())

    def _extract_json_string(self, usd_prim):
        json_data = usd_prim.GetAttribute('jsonData').Get()
        print(usd_prim)
        self.jsonData = json.loads(json_data)
        print("SELF     =",self.jsonData)

    def _report(self, usd_prim, usd_path):
        if Options.verbose:
            prim_type = usd_prim.GetTypeName()
            print(f'Created {prim_type} at {usd_path}')
