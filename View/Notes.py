import pygame
import cv2
import numpy
import NoteQueue

class Notes:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        self.C4 = pygame.mixer.Sound("Notes/C4.wav")
        self.Db4 = pygame.mixer.Sound("Notes/Db4.wav")
        self.D4 = pygame.mixer.Sound("Notes/D4.wav")
        self.Eb4 = pygame.mixer.Sound("Notes/Eb4.wav")
        self.E4 = pygame.mixer.Sound("Notes/E4.wav")
        self.F4 = pygame.mixer.Sound("Notes/F4.wav")
        self.Gb4 = pygame.mixer.Sound("Notes/Gb4.wav")
        self.G4 = pygame.mixer.Sound("Notes/G4.wav")
        self.Ab4 = pygame.mixer.Sound("Notes/Ab4.wav")
        self.A4 = pygame.mixer.Sound("Notes/A4.wav")
        self.Bb4 = pygame.mixer.Sound("Notes/Bb4.wav")
        self.B4 = pygame.mixer.Sound("Notes/B4.wav")

        self.allNotes = {
            "C1": self.C4,
            "Db1": self.Db4,
            "D1": self.D4,
            "Eb1": self.Eb4,
            "E1": self.E4,
            "F1": self.F4,
            "Gb1": self.Gb4,
            "G1": self.G4,
            "Ab1": self.Ab4,
            "A1": self.A4,
            "Bb1": self.Bb4,
            "B1": self.B4,
        }

        self.noteQueue = NoteQueue.NoteQueue()


    def addToQueue(self, note):
        self.noteQueue.put(note)


    def removeFromQueue(self, note):
        self.noteQueue.remove(note)

    def getOldestNote(self):
        return self.noteQueue.get()

    def checkQueueFull(self, queue, note):
        if queue.qsize() == 8:
            note = queue.get()
            note.stop()
        queue.put(note)
