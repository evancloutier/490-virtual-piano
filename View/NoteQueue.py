
class NoteQueue:
    def __init__(self):
        self.noteQueue = dict()
        self.size = 0
        self.max = 8

    def remove(self, item):
        if item in self.noteQueue:
            idx = self.noteQueue[item]
            del self.noteQueue[item]
            for key in self.noteQueue:
                if self.noteQueue[key] >= idx:
                    self.noteQueue[key] -= 1
            self.size -= 1

    def put(self, item):
        #if note already being played, stop it and replay
        self.remove(item)

        #check if max number of notes are already being played
        if self.size == self.max:
            self.get()

        maxIdx = max(self.noteQueue, key=lambda i: self.noteQueue[i])
        self.noteQueue[item] = maxIdx + 1
        self.size += 1

    def get(self):
        note = None
        if self.size > 0:
            for key in self.noteQueue:
                if self.noteQueue[key] == 1:
                    note = key
                    del self.noteQueue[key]
            for key in self.noteQueue:
                self.noteQueue[key] -= 1
            self.size -= 1


