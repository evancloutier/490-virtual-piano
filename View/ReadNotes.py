import os
import pdb

class ReadNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = None

    def readNotes(self):
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

readNotes = ReadNotes()
