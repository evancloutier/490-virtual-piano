
class WriteNotes:
    def __init__(self):
        self.fileLocation = "../Model/Keys.txt"
        self.file = open(self.fileLocation, 'w+')
        self.file.close()

    def writeKeyNamesToFile(self, keyList):
        self.file = open(self.fileLocation, 'w+')
        self.file.write(str(keyList))
        self.file.close()
