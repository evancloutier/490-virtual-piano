import os
import pdb

class ReadNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = None
        self.oldNotes = set()

    def readNotes(self):
        notes = []
        if os.path.exists(self.fileLocation):
            self.file = open(self.fileLocation)

            raw = self.file.readlines()
            if len(raw) > 0:
                raw = raw[0]
                raw = raw[1:-1]
                raw = raw.replace("'", "")
                notes = raw.split(",")
                for idx in range(len(notes)):
                    notes[idx] = notes[idx].strip()

            self.file.close()
        notes = self.getNewNotes(notes)
        return notes

    def getNewNotes(self, newNotes):
        newNotesCopy = newNotes[:]
        newNotes = set(newNotes)
        newNotes = newNotes - self.oldNotes
        self.oldNotes = set(newNotesCopy)
        return list(newNotes)
