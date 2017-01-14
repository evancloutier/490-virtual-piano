class KeyDetector:
        
    data = []
    
    def __init__(self):
        data = []
    
    def receiveFrame(self, frame):
        self.data = frame
    
    def transmitFrame(self):
        return self.data.asarray()