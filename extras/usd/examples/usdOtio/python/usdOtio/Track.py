

class Track:
    def __init__(self):
        self.children = []
        self.jsonData = {}

    def append_child(self, child):
        self.children.append(child)
        
    def from_json_string(self, s):
        self.jsonData = json.loads(s)
        # Remove children
        self.jsonData.pop('children')

    def to_json_string(self):
        self.jsonData['children'] = '[';
        json_strings = [child.to_json_string() for child in self.children]
        self.jsonData['children'] += ','.join(json_strings)
        self.jsonData['children'] += ']';
        return json.dumps(self.jsonData)
