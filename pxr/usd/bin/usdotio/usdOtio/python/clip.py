

import json

import opentimelineio as otio
    
from usdOtio.box2d_mixin import Box2dMixin
from usdOtio.external_reference import ExternalReference
from usdOtio.image_sequence_reference import ImageSequenceReference
from usdOtio.item import Item
from usdOtio.missing_reference import MissingReference
from usdOtio.options import Options, Verbose

class Clip(Item, Box2dMixin):

    FILTER_KEYS = [
        'media_references',
        'available_image_bounds',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.media_references = {}
        self.enabled = True
        if self.otio_item:
            self.enabled = otio_item.enabled

    def append_media_reference(self, ref_prim, key = 'DEFAULT_MEDIA'):
        self.media_references[key] = ref_prim
    
    def from_usd(self, usd_prim):
        super().from_usd(usd_prim)
        
        #
        # Traverse the stage to get the jsonData of each node
        #
        for x in usd_prim.GetChildren():
            usd_name = x.GetName()
            usd_type = x.GetTypeName()
            if usd_type == 'OtioExternalReference':
                ref_prim = ExternalReference()
                ref_prim.from_usd(x)
                self.append_media_reference(ref_prim)
            elif usd_type == 'OtioImageSequenceReference':
                ref_prim = ImageSequenceReference()
                ref_prim.from_usd(x)
                self.append_media_reference(ref_prim)
            elif usd_type == 'OtioMissingReference':
                ref_prim = MissingReference()
                ref_prim.from_usd(x)
                self.append_media_reference(ref_prim)
            elif usd_type == 'OtioBox2d':
                ref_prim = Box2d()
                self.imaging_bounds = ref_prim.from_usd(x)
            else:
                pass

        newdict = {}
        for key, val in self.media_references.items():
            newval = json.loads(val.to_json_string())
            newdict[key] = newval
    
        self.jsonData['media_references'] = newdict
        
        return self.jsonData

    
    def to_usd(self, stage, usd_path): 
        super().to_usd(stage, usd_path)
        
        self._set_box2d(stage, usd_path, 'available_image_bounds')
            
        usd_prim = self._create_usd(stage, usd_path, 'OtioClip')
        
        m = self.otio_item.media_reference
        if m:
            media_prim = None
            media_path = usd_path + '/media_reference'
            if isinstance(m, otio.schema.MissingReference):
                media_path = usd_path + '/missing_reference'
                media_prim = MissingReference(m)
                media_prim.to_usd(stage, media_path)
            elif isinstance(m, otio.schema.ExternalReference):
                media_path = usd_path + '/external_reference'
                media_prim = ExternalReference(m)
                media_prim.to_usd(stage, media_path)
            elif isinstance(m, otio.schema.ImageSequenceReference):
                media_path = usd_path + '/image_sequence_reference'
                media_prim = ImageSequenceReference(m)
                media_prim.to_usd(stage, media_path)
            else:
                print(f'WARNING: {m} is invalid!')

        return usd_prim


    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(Clip.FILTER_KEYS)
