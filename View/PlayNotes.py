import ReadNotes
import pygame
import Notes
import pdb

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
            #print "new:", newNotes
            #print "released:", releasedNotes
            for newNote in newNotes:
                if newNote != "" and len(newNote) != 0:
                    notesToPlay.append(self.musicalNotes.allNotes[newNote])

            for releasedNote in releasedNotes:
                if releasedNote != "" and len(newNote) != 0:
                    notesToRelease.append(self.musicalNotes.allNotes[releasedNote])

            for noteToPlay in notesToPlay:
                self.musicalNotes.addToQueue(noteToPlay)
                noteToPlay.stop()
                noteToPlay.play()

            for noteToRelease in notesToRelease:

                self.musicalNotes.removeFromQueue(noteToRelease)
                noteToRelease.stop()


    def getNewNotes(self, newNotes):
        newNotes = newNotes - self.prevNotes
        return newNotes

player = PlayNotes()
player.playNotes()
