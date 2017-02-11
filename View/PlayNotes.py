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
            audioNotes = []
            noteNames = self.readNotes.readNotes()
            print noteNames
            for noteName in noteNames:
                if noteName != "":
                    audioNotes.append(self.musicalNotes.allNotes[noteName])

            for audioNote in audioNotes:
                self.musicalNotes.checkQueueFull(self.musicalNotes.noteQueue, audioNote)
                audioNote.stop()
                audioNote.play()

    def getNewNotes(self, newNotes):
        newNotes = newNotes - self.prevNotes
        return newNotes

player = PlayNotes()
player.playNotes()
