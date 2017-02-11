
class WriteNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = open(self.fileLocation, 'w+')
        self.oldKeys = None
        self.file.close()

    def writeNewKeyNamesToFile(self, newKeys):
        newKeysCopy = newKeys[:]
        if self.oldKeys is not None:
            diffKeys = set(newKeys) - self.oldKeys
            newKeys = list(diffKeys)

        self.oldKeys = set(newKeysCopy)

        self.file = open(self.fileLocation, 'w+')
        self.file.write(str(newKeys))
        self.file.close()
