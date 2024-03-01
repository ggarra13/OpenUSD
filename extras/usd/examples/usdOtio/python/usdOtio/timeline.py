
import json
from usdOtio.base import Base

class Timeline(Base):
    def __init__(self, otio_item = None):
        super().__init__(otio_item)
        self.tracks = []
        self.jsonData.pop('tracks')

    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        json_strings = [track.to_json_string() for track in self.tracks]
        self.jsonData['tracks'] = json_strings
        return json.dumps(self.jsonData)

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTimeline')
        if self.verbose:
            print(f'Created Timeline at {usd_path}')
        self._store_json_string(usd_path, usd_prim)
        return usd_prim
