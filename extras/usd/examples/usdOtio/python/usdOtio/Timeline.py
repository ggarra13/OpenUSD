
from usdOtio import Base

class Timeline(usdOtio.Base):
    def __init__(self):
        self.tracks = []
        self.jsonData = {}

    def __init__(self, otio_item):
        self.tracks = []
        self.jsonData = otio_item.to_json_string()
        # Remove tracks
        self.jsonData.pop('tracks')

    def append_track(self, track):
        self.tracks.append(track)

    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        json_strings = [track.to_json_string() for track in self.tracks]
        self.jsonData['tracks'] = json_strings
        return json.dumps(self.jsonData)

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioTimeline')
        return usd_prim
