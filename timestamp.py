

class Timestamp:
    def __init__(self, time, location):
        self.time = time
        self.location = location
    def __repr__(self):
        return (self.time, self.location)

