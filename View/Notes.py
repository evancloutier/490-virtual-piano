import pygame
import cv2
import numpy
import Queue

pygame.mixer.init()
pygame.init()

class Notes:
    def __init__(self):
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
            "C4": self.C4,
            "Db4": self.Db4,
            "D4": self.D4,
            "Eb4": self.Eb4,
            "E4": self.E4,
            "F4": self.F4,
            "Gb4": self.Gb4,
            "G4": self.G4,
            "Ab4": self.Ab4,
            "A4": self.A4,
            "Bb4": self.Bb4,
            "B4": self.B4,
        }

        self.noteQueue = Queue.Queue()

    def checkQueueFull(self, queue, note):
        if queue.qsize() == 8:
            note = queue.get()
            note.stop()
        queue.put(note)

    def cv2Play(self):
        im = numpy.zeros((200,200))
        while True:
            cv2.imshow('im',im)
            k = cv2.waitKey(10)


            if k == ord('q'):
                self.checkQueueFull(self.noteQueue, self.C4)
                self.C4.stop()
                self.C4.play()
            elif k == ord('w'):
                self.checkQueueFull(self.noteQueue, self.Db4)
                self.Db4.stop()
                self.Db4.play()
            elif k == ord('e'):
                self.checkQueueFull(self.noteQueue, self.D4)
                self.D4.stop()
                self.D4.play()
            elif k == ord('r'):
                self.checkQueueFull(self.noteQueue, self.Eb4)
                self.Eb4.stop()
                self.Eb4.play()
            elif k == ord('t'):
                self.checkQueueFull(self.noteQueue, self.E4)
                self.E4.stop()
                self.E4.play()
            elif k == ord('y'):
                self.checkQueueFull(self.noteQueue, self.F4)
                self.F4.stop()
                self.F4.play()
            elif k == ord('u'):
                self.checkQueueFull(self.noteQueue, self.Gb4)
                self.Gb4.stop()
                self.Gb4.play()
            elif k == ord('i'):
                self.checkQueueFull(self.noteQueue, self.G4)
                self.G4.stop()
                self.G4.play()
            elif k == ord('o'):
                self.checkQueueFull(self.noteQueue, self.Ab4)
                self.Ab4.stop()
                self.Ab4.play()
            elif k == ord('p'):
                self.checkQueueFull(self.noteQueue, self.A4)
                self.A4.stop()
                self.A4.play()
            elif k == ord('a'):
                self.checkQueueFull(self.noteQueue, self.Bb4)
                self.Bb4.stop()
                self.Bb4.play()
            elif k == ord('s'):
                self.checkQueueFull(self.noteQueue, self.B4)
                self.B4.stop()
                self.B4.play()

            elif k == 27:
                break

notes = Notes()
notes.cv2Play()