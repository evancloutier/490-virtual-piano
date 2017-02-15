import cv2
import numpy as np
import imutils
import pdb

class KeyDetector:

    def __init__(self, kinect, firstNote):
        self.kinect = kinect
        self.lowerThresh = 200
        self.upperThresh = 255
        self.keys = dict()

        while True:
            self.frames = self.kinect.getFrame()
            color = self.frames["color"]
            self.bounded = color
            self.getKeyContours()
            self.assignContourToKey(firstNote)
            cv2.imshow("Color", cv2.resize(self.bounded, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27 or k == 1048603:
                cv2.destroyAllWindows()
                break
            elif k == ord('q'):
                if self.lowerThresh > 0:
                    self.lowerThresh -= 1
                    print "lowerThresh", self.lowerThresh
            elif k == ord('w'):
                if self.lowerThresh < 255:
                    self.lowerThresh += 1
                    print "lowerThresh", self.lowerThresh
            elif k == ord('a'):
                if self.upperThresh > 0:
                    self.upperThresh -= 1
                    print "upperThresh", self.upperThresh
            elif k == ord('s'):
                if self.upperThresh < 255:
                    self.upperThresh += 1
                    print "upperThresh", self.upperThresh

    def assignContourToKey(self, firstNote):
        #sorted from left to right from player perspective
        self.keys = dict()
        noteNames = ["C","Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        noteIdx = noteNames.index(firstNote)

        for idx, contour in enumerate(self.contours):
            noteName = noteNames[noteIdx]
            noteOctave = idx / len(noteNames) + 1
            noteName += str(noteOctave)
            self.keys[noteName] = contour[0][:]

            noteIdx = (noteIdx + 1) % len(noteNames)

        print "num keys detected:", len(self.keys)


    def getKeyContours(self):
        gray = cv2.cvtColor(self.bounded, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, self.lowerThresh, self.upperThresh, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
        cv2.imshow("Threshold", cv2.resize(thresh, (int(1920 / 3), int(1080 / 3))))

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        contours = []

        for idx, c in enumerate(cnts):
            M = cv2.moments(c)

            # Eliminate the contour if the moment is zero
            if all(x == 0 for x in M.values()):
                continue

            # Eliminate smaller contours based on area
            if int(M["m00"]) < 500:
                continue
            else:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                contour = [c, cX, cY]
                contours.append(contour)
        contours.sort(key = lambda x: x[1])
        self.contours = contours
