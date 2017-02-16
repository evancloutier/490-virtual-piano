import pygame
import cv2
import numpy
import NoteQueue
import pdb

class Notes:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()

        self.instruments = {
            'Piano': 'Piano',
            'Xylphone': 'Xylophone',
        }

        self.directions = {
            "Up": 1,
            "Down": -1
        }

        self.baseNotes = ["C1","Db1","D1","Eb1","E1","F1","Gb1","G1","Ab1","A1","Bb1","B1",
                          "C2","Db2","D2","Eb2","E2","F2","Gb2","G2","Ab2","A2","Bb2","B2",]

        self.currInstrument = "Piano"


        self.pianoC3 = pygame.mixer.Sound("Piano/C3.wav")
        self.pianoDb3 = pygame.mixer.Sound("Piano/Db3.wav")
        self.pianoD3 = pygame.mixer.Sound("Piano/D3.wav")
        self.pianoEb3 = pygame.mixer.Sound("Piano/Eb3.wav")
        self.pianoE3 = pygame.mixer.Sound("Piano/E3.wav")
        self.pianoF3 = pygame.mixer.Sound("Piano/F3.wav")
        self.pianoGb3 = pygame.mixer.Sound("Piano/Gb3.wav")
        self.pianoG3 = pygame.mixer.Sound("Piano/G3.wav")
        self.pianoAb3 = pygame.mixer.Sound("Piano/Ab3.wav")
        self.pianoA3 = pygame.mixer.Sound("Piano/A3.wav")
        self.pianoBb3 = pygame.mixer.Sound("Piano/Bb3.wav")
        self.pianoB3 = pygame.mixer.Sound("Piano/B3.wav")

        self.pianoC4 = pygame.mixer.Sound("Piano/C4.wav")
        self.pianoDb4 = pygame.mixer.Sound("Piano/Db4.wav")
        self.pianoD4 = pygame.mixer.Sound("Piano/D4.wav")
        self.pianoEb4 = pygame.mixer.Sound("Piano/Eb4.wav")
        self.pianoE4 = pygame.mixer.Sound("Piano/E4.wav")
        self.pianoF4 = pygame.mixer.Sound("Piano/F4.wav")
        self.pianoGb4 = pygame.mixer.Sound("Piano/Gb4.wav")
        self.pianoG4 = pygame.mixer.Sound("Piano/G4.wav")
        self.pianoAb4 = pygame.mixer.Sound("Piano/Ab4.wav")
        self.pianoA4 = pygame.mixer.Sound("Piano/A4.wav")
        self.pianoBb4 = pygame.mixer.Sound("Piano/Bb4.wav")
        self.pianoB4 = pygame.mixer.Sound("Piano/B4.wav")

        self.pianoC5 = pygame.mixer.Sound("Piano/C5.wav")
        self.pianoDb5 = pygame.mixer.Sound("Piano/Db5.wav")
        self.pianoD5 = pygame.mixer.Sound("Piano/D5.wav")
        self.pianoEb5 = pygame.mixer.Sound("Piano/Eb5.wav")
        self.pianoE5 = pygame.mixer.Sound("Piano/E5.wav")
        self.pianoF5 = pygame.mixer.Sound("Piano/F5.wav")
        self.pianoGb5 = pygame.mixer.Sound("Piano/Gb5.wav")
        self.pianoG5 = pygame.mixer.Sound("Piano/G5.wav")
        self.pianoAb5 = pygame.mixer.Sound("Piano/Ab5.wav")
        self.pianoA5 = pygame.mixer.Sound("Piano/A5.wav")
        self.pianoBb5 = pygame.mixer.Sound("Piano/Bb5.wav")
        self.pianoB5 = pygame.mixer.Sound("Piano/B5.wav")

        self.pianoC6 = pygame.mixer.Sound("Piano/C6.wav")
        self.pianoDb6 = pygame.mixer.Sound("Piano/Db6.wav")
        self.pianoD6 = pygame.mixer.Sound("Piano/D6.wav")
        self.pianoEb6 = pygame.mixer.Sound("Piano/Eb6.wav")
        self.pianoE6 = pygame.mixer.Sound("Piano/E6.wav")
        self.pianoF6 = pygame.mixer.Sound("Piano/F6.wav")
        self.pianoGb6 = pygame.mixer.Sound("Piano/Gb6.wav")
        self.pianoG6 = pygame.mixer.Sound("Piano/G6.wav")
        self.pianoAb6 = pygame.mixer.Sound("Piano/Ab6.wav")
        self.pianoA6 = pygame.mixer.Sound("Piano/A6.wav")
        self.pianoBb6 = pygame.mixer.Sound("Piano/Bb6.wav")
        self.pianoB6 = pygame.mixer.Sound("Piano/B6.wav")

        self.xylophoneC5 = pygame.mixer.Sound("Xylophone/C5.wav")
        self.xylophoneDb5 = pygame.mixer.Sound("Xylophone/Db5.wav")
        self.xylophoneD5 = pygame.mixer.Sound("Xylophone/D5.wav")
        self.xylophoneEb5 = pygame.mixer.Sound("Xylophone/Eb5.wav")
        self.xylophoneE5 = pygame.mixer.Sound("Xylophone/E5.wav")
        self.xylophoneF5 = pygame.mixer.Sound("Xylophone/F5.wav")
        self.xylophoneGb5 = pygame.mixer.Sound("Xylophone/Gb5.wav")
        self.xylophoneG5 = pygame.mixer.Sound("Xylophone/G5.wav")
        self.xylophoneAb5 = pygame.mixer.Sound("Xylophone/Ab5.wav")
        self.xylophoneA5 = pygame.mixer.Sound("Xylophone/A5.wav")
        self.xylophoneBb5 = pygame.mixer.Sound("Xylophone/Bb5.wav")
        self.xylophoneB5 = pygame.mixer.Sound("Xylophone/B5.wav")

        self.xylophoneC6 = pygame.mixer.Sound("Xylophone/C6.wav")
        self.xylophoneDb6 = pygame.mixer.Sound("Xylophone/Db6.wav")
        self.xylophoneD6 = pygame.mixer.Sound("Xylophone/D6.wav")
        self.xylophoneEb6 = pygame.mixer.Sound("Xylophone/Eb6.wav")
        self.xylophoneE6 = pygame.mixer.Sound("Xylophone/E6.wav")
        self.xylophoneF6 = pygame.mixer.Sound("Xylophone/F6.wav")
        self.xylophoneGb6 = pygame.mixer.Sound("Xylophone/Gb6.wav")
        self.xylophoneG6 = pygame.mixer.Sound("Xylophone/G6.wav")
        self.xylophoneAb6 = pygame.mixer.Sound("Xylophone/Ab6.wav")
        self.xylophoneA6 = pygame.mixer.Sound("Xylophone/A6.wav")
        self.xylophoneBb6 = pygame.mixer.Sound("Xylophone/Bb6.wav")
        self.xylophoneB6 = pygame.mixer.Sound("Xylophone/B6.wav")

        self.allPianoNotes = [self.pianoC3, self.pianoDb3, self.pianoD3, self.pianoEb3, self.pianoE3, self.pianoF3, self.pianoGb3, self.pianoG3, self.pianoAb3, self.pianoA3, self.pianoBb3, self.pianoB3,
                              self.pianoC4, self.pianoDb4, self.pianoD4, self.pianoEb4, self.pianoE4, self.pianoF4, self.pianoGb4, self.pianoG4, self.pianoAb4, self.pianoA4, self.pianoBb4, self.pianoB4,
                              self.pianoC5, self.pianoDb5, self.pianoD5, self.pianoEb5, self.pianoE5, self.pianoF5, self.pianoGb5, self.pianoG5, self.pianoAb5, self.pianoA5, self.pianoBb5, self.pianoB5,
                              self.pianoC6, self.pianoDb6, self.pianoD6, self.pianoEb6, self.pianoE6, self.pianoF6, self.pianoGb6, self.pianoG6, self.pianoAb6, self.pianoA6, self.pianoBb6, self.pianoB6,]

        self.allXylophoneNotes = [self.xylophoneC5, self.xylophoneDb5, self.xylophoneD5, self.xylophoneEb5, self.xylophoneE5, self.xylophoneF5, self.xylophoneGb5, self.xylophoneG5, self.xylophoneAb5, self.xylophoneA5, self.xylophoneBb5, self.xylophoneB5,
                                  self.xylophoneC6, self.xylophoneDb6, self.xylophoneD6, self.xylophoneEb6, self.xylophoneE6, self.xylophoneF6, self.xylophoneGb6, self.xylophoneG6, self.xylophoneAb6, self.xylophoneA6, self.xylophoneBb6, self.xylophoneB6]

        self.allNotes = dict()
        self.noteQueue = NoteQueue.NoteQueue()
        self.currOctave = 5
        self.buildAllNotesFromInstrumentAndOctave(self.currInstrument, self.currOctave)


    def addToQueue(self, note):
        self.noteQueue.put(note)


    def buildAllNotesFromInstrumentAndOctave(self, instrument, octave):
        if instrument == "Piano":
            if octave >= 3 and octave <= 5:
                self.allNotes = dict()
                octaveIdx = octave - 3

                for baseNote, instrumentNote in zip(self.baseNotes, self.allPianoNotes[octaveIdx * 12:]):
                    self.allNotes[baseNote] = instrumentNote

        elif instrument == "Xylophone":
            print "yea we hur"
            if octave == 5:
                self.allNotes = dict()
                octaveIdx = 0
                for baseNote, instrumentNote in zip(self.baseNotes, self.allXylophoneNotes[octaveIdx * 12:]):
                    self.allNotes[baseNote] = instrumentNote



    def removeFromQueue(self, note):
        self.noteQueue.remove(note)

    def getOldestNote(self):
        return self.noteQueue.get()

    def checkQueueFull(self, queue, note):
        if queue.qsize() == 8:
            note = queue.get()
            note.stop()
        queue.put(note)
