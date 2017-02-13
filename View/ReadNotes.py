import os
import pdb

class ReadNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = None
        self.notes = []
        self.newNotes = []
        self.releasedNotes = []
        self.oldNotes = set()

    def readNotes(self):
        self.notes = []
        newNotes = []
        releasedNotes = []
        if os.path.exists(self.fileLocation):
            self.file = open(self.fileLocation)

            raw = self.file.readlines()
            if len(raw) > 0:
                raw = raw[0]
                raw = raw[1:-1]
                raw = raw.replace("'", "")
                self.notes = raw.split(",")
                for idx in range(len(self.notes)):
                    self.notes[idx] = self.notes[idx].strip()

                origNotes = self.notes[:]
                newNotes = self.getNewNotes(self.notes[:])
                self.newNotes = newNotes
                releasedNotes = self.getReleasedNotes(self.notes[:])
                self.releasedNotes = releasedNotes
                self.oldNotes = set(origNotes)
            self.file.close()

        return (newNotes, releasedNotes)

    def getNewNotes(self, newNotes):
        newNotes = set(newNotes)
        newNotes = newNotes - self.oldNotes
        return list(newNotes)

    def getReleasedNotes(self, allNotes):
        allNotes = set(allNotes)
        releasedNotes = self.oldNotes - allNotes
        return list(releasedNotes)
