
from usdOtio import Base

class Stack(usdOtio.Base):
    def __init__(self):
        self.children = []
        self.jsonData = {}

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
        # Remove children from jsonData
        self.jsonData.pop('children')

    def to_json_string(self):
        json_strings = [child.to_json_string() for child in self.children]
        self.jsonData['children'] = json_strings
        return json.dumps(self.jsonData)

    def to_usd(self, stage, usd_path):
        usd_prim = stage.DefinePrim(usd_path, 'OtioStack')
        return usd_prim
