import pdb
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

        maxVal = 0
        for k in self.noteQueue:
            if self.noteQueue[k] > maxVal:
                maxVal = self.noteQueue[k]
        self.noteQueue[item] = maxVal + 1
        self.size += 1

    def get(self):
        note = None
        noteToDel = None
        if self.size > 0:
            for key in self.noteQueue:
                if self.noteQueue[key] == 1:
                    noteToDel = key
            del self.noteQueue[noteToDel]
            for key in self.noteQueue:
                self.noteQueue[key] -= 1
            self.size -= 1
