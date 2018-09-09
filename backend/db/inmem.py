class InMem():
    def __init__(self):
        self.data = {}
    def delete(self, resource_id):
        self.data.pop(resource_id)
    def get(self):
        return self.data
    def set(self, json):
        self.data.update(json)
