
class WriteNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = open(self.fileLocation, 'w+')
        self.oldKeys = None
        self.file.close()

    def writeKeyNamesToFile(self, keys):
        self.file = open(self.fileLocation, 'w+')
        self.file.write(str(keys))
        self.file.close()
