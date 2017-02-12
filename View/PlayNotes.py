import ReadNotes
import pygame
import Notes

class PlayNotes:
    def __init__(self):
        self.readNotes = ReadNotes.ReadNotes()
        self.musicalNotes = Notes.Notes()
        self.prevNotes = set()

    def playNotes(self):
        while True:
            notesToPlay = []
            notesToRelease = []
            newNotes, releasedNotes = self.readNotes.readNotes()
            print "new:", newNotes
            print "released:", releasedNotes
            for newNote in newNotes:
                if newNote != "":
                    notesToPlay.append(self.musicalNotes.allNotes[newNote])

            for releasedNote in releasedNotes:
                if releasedNote != "":
                    notesToRelease.append(self.musicalNotes.allNotes[releasedNote])


            for newNote in newNotes:
                self.musicalNotes.addToQueue(self.musicalNotes.noteQueue, newNote)
                newNote.stop()
                newNote.play()

            for releasedNote in releasedNotes:
                self.musicalNotes.removeFromQueue(self.musicalNotes.noteQueue, releasedNote)
                releasedNote.stop()


    def getNewNotes(self, newNotes):
        newNotes = newNotes - self.prevNotes
        return newNotes

player = PlayNotes()
player.playNotes()
