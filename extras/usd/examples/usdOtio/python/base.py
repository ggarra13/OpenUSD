
import json

import pxr

import opentimelineio as otio

from usdOtio.options import Options, Verbose

class Base:

    ATTRIBUTES = [
        'OTIO_SCHEMA',
        ]
    
    def __init__(self, otio_item = None):
        self.jsonData = {}
        self.otio_item = otio_item
        self.usd_prim  = None
        if otio_item:
            self.from_json_string(otio_item.to_json_string())
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        return json.dumps(self.jsonData)

    def from_usd(self, usd_prim):
        self._get_attributes(usd_prim)
        return self.jsonData

    def to_usd(self, stage, usd_path):
        pass
    
    def create_usd(self, stage, usd_path, usd_type):
        usd_prim = stage.DefinePrim(usd_path, usd_type)
        if Options.verbose == Verbose.INFO:
            print(f'Created {usd_prim}')
        self._set_attributes(usd_prim)
        self._report(usd_prim, usd_path)
        return usd_prim

    
    
    def filter_keys(self):
        pass
    
    def _set_attribute(self, usd_prim, key, value):
        if Options.verbose == Verbose.VERBOSE:
            print(f'\t\tSetting {key} = {value}')
        attr = usd_prim.GetAttribute(key)
        if isinstance(value, dict):
            value = json.dumps(value)
        elif value is None:
            value = json.dumps(value)

        try:
            attr.Set(value)
        except pxr.Tf.ErrorException:
            usd_type = usd_prim.GetTypeName()
            print(f'WARNING: Unknown attribute {key} for {usd_type} at')
            print(f'{usd_prim}')
            print(f'Valid Properties:')
            for i in usd_prim.GetPropertyNames():
                print(f'\t{i}')
            unknown = usd_prim.GetAttribute('unknown').Get()
            if not unknown:
                unknown = '{}'
            if isinstance(unknown, str):
                unknown_dict = json.loads(unknown)
                unknown_dict[key] = value
                self._set_attribute(usd_prim, 'unknown', unknown_dict)
            
    def _set_attributes(self, usd_prim):
        self.filter_keys()
        
        if self.jsonData and len(self.jsonData) > 0:
            for key, val in self.jsonData.items():
                self._set_attribute(usd_prim, key, val)
    
    def _get_attribute(self, usd_prim, key):
        val = usd_prim.GetAttribute(key).Get()
        self.jsonData[key] = val
        
    def _get_attributes(self, usd_prim):
        attrs = usd_prim.GetPropertyNames()
        for attr in attrs:
            if attr == 'unknown':
                continue
            self._get_attribute(usd_prim, attr)

        self._get_attribute(usd_prim, 'unknown')
        unknown = self.jsonData['unknown']
        if unknown and len(unknown) > 0:
            unknown_dict = json.loads(unknown)
            for key, val in unknown_dict.items():
                if key == 'unknown':
                    continue
                if Options.verbose == Verbose.DEBUG: 
                    print(f'\tGetting {key} = {val})')
                self.jsonData[key] = val

        del self.jsonData['unknown']
         
    def _report(self, usd_prim, usd_path):
        if Options.verbose == Verbose.INFO:
            prim_type = usd_prim.GetTypeName()
            print(f'\tCreated {prim_type} at {usd_path}')

    def _filter_keys(self, keys):
        for key in keys:
            self.jsonData.pop(key, None)
