
import json

from usdOtio.media_reference import MediaReference

class ImageSequenceReference(MediaReference):

    FILTER_KEYS = [
        'missing_frame_policy',
    ]
    
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
    
    def to_usd(self, stage, usd_path):
        super().to_usd(stage, usd_path)
        usd_prim = self._create_usd(stage, usd_path,
                                   'OtioImageSequenceReference')
        return usd_prim

    def _filter_keys(self):
        super()._filter_keys()
        self._remove_keys(ImageSequenceReference.FILTER_KEYS)

    def _set_attributes(self, usd_prim):
        
        # USD does not accept variant sets in schemas
        policy = self.jsonData['missing_frame_policy']
        policy = policy.removeprefix('MissingFramePolicy.')
        self._set_attribute(usd_prim, 'missing_frame_policy', policy) 
        
        super()._set_attributes(usd_prim)
