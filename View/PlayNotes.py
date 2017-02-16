import ReadNotes
import pygame
import Notes
import pdb

class PlayNotes:
    def __init__(self):
        self.readNotes = ReadNotes.ReadNotes()
        self.musicalNotes = Notes.Notes()
        self.prevNotes = set()

    def updateInstrument(self, alexaFeedback):
        if len(alexaFeedback) > 0:
            alexaFeedback = alexaFeedback[0].upper() + alexaFeedback[1:]
            print alexaFeedback
        if alexaFeedback == "Up":
            self.musicalNotes.buildAllNotesFromInstrumentAndOctave(self.musicalNotes.currInstrument, self.musicalNotes.currOctave + 1)

        elif alexaFeedback == "Down":
            self.musicalNotes.buildAllNotesFromInstrumentAndOctave(self.musicalNotes.currInstrument, self.musicalNotes.currOctave - 1)

        elif alexaFeedback == "Piano":
            if self.musicalNotes.currInstrument != "Piano":
                self.musicalNotes.currOctave = 4
                self.musicalNotes.currInstrument = "Piano"
                self.musicalNotes.buildAllNotesFromInstrumentAndOctave(alexaFeedback, 4)

        elif alexaFeedback == "Xylophone":
            if self.musicalNotes.currInstrument != "Xylophone":
                self.musicalNotes.currOctave = 5
                self.musicalNotes.currInstrument = "Xylophone"
                self.musicalNotes.buildAllNotesFromInstrumentAndOctave(alexaFeedback, 5)

        elif alexaFeedback == "Trumpet":
            if self.musicalNotes.currInstrument != "Trumpet":
                self.musicalNotes.currOctave = 4
                self.musicalNotes.currInstrument = "Trumpet"
                self.musicalNotes.buildAllNotesFromInstrumentAndOctave(alexaFeedback, 4)



    def playNotes(self):
        while True:
            notesToPlay = []
            notesToRelease = []
            newNotes, releasedNotes = self.readNotes.readNotes()
            print "new notes:", newNotes
            alexaFeedback = self.readNotes.readAlexa()
            self.updateInstrument(alexaFeedback)

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
