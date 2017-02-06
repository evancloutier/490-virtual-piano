import cv2
import time
import numpy as np
import math
import os, sys
import imutils
import pdb

width = 1920
height = 1080

class FingerDetectorEvan:

    def __init__(self, kinect):
        self.kinect = kinect
        self.blur = 7
        self.lowThresh = 159
        self.highThresh = 255
        self.histogram = None

    def drawCenterOfHand(self, centerOfHand):
        if centerOfHand is not None:
            if type(centerOfHand) == np.ndarray:
                centerOfHand = (centerOfHand[0][0], centerOfHand[0][1])
            cv2.circle(self.color, centerOfHand, 3, (0, 255, 0), 2)

    def getSkinSamples(self):
        sampleWidth = 100
        sampleHeight = 200
        numSamples = 9

        startWidth = (width - sampleWidth) / 2
        startHeight = (height - sampleHeight) / 2

        numCol = int(math.sqrt(numSamples))
        numRow = int(math.sqrt(numSamples))

        colWidth = sampleWidth / numCol
        rowHeight = sampleHeight / numRow

        currCol = 0
        currRow = 0
        currWidth = 0
        currHeight = 0

        sampleCenters = []

        for sample in range(numSamples):
            currRow = sample / numRow
            currCol = sample % numCol

            currHeight = startHeight + (currRow * rowHeight)
            currWidth = startWidth + (currCol * colWidth)

            self.drawCenterOfHand((currWidth, currHeight))
            sampleCenters.append([currWidth, currHeight])

        return sampleCenters

    def getHandColors(self, frame, samplePoints):
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = np.zeros(frame.shape[:2], np.uint8)

        # Should this radius value reflect the sample points drawn?
        radius = 5

        # Can this be improved?
        for x, y in samplePoints:
            for xIdx in range(x - radius, x + radius):
                for yIdx in range(y - radius, y + radius):
                    mask.itemset((xIdx, yIdx), 255)

        masked = cv2.bitwise_and(frame, frame, mask = mask)

        hist = cv2.calcHist([hsv], [0], mask, [256], [0, 256])
        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

        return hist

    def buildSkinColorHistogram(self):
        handHistogram = None

        while True:
            self.frames = self.kinect.getFrame()
            self.color = self.frames["color"]
            copy = np.copy(self.color)

            samplePoints = self.getSkinSamples()

            cv2.imshow("Skin Color", cv2.resize(self.color, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.histogram = self.getHandColors(copy, samplePoints)
                break

    def getLargestShapes(self, frame, bothHands = False):
        cnts = cv2.findContours(frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        contours = []

        print len(cnts)

        for contour in cnts:
            M = cv2.moments(contour)

            if all(x == 0 for x in M.values()):
                continue

            if int(M["m00"] < 500):
                continue
            else:
                contours.append(contour)

        print len(contours)
        print "--------------"



    def applyHistogram(self, frame):
        row, col, dep = frame.shape
        black = np.zeros((row, col, dep), np.uint8)
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # What does the range passed in represent?
        filtered = cv2.calcBackProject([hsv], [0], self.histogram, [0, 180, 0, 256], 1)
        filtered = cv2.medianBlur(filtered, self.blur)

        hands = self.getLargestShapes(filtered)
