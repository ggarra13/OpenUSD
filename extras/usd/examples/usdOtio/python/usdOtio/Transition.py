

class Transition:
    def __init__(self):
        pass

    def __init__(self, otio_item):
        self.jsonData = otio_item.to_json_string()
    
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        
    def to_json_string(self):
        return json.dumps(self.jsonData)
