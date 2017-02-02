import cv2
import math
import numpy as np
import imutils
import pdb

width = 1920
height = 1080

class BoundsDetector:

    def __init__(self, kinect):
        self.kinect = kinect
        self.lowerThresh = 225
        self.upperThresh = 255

        while True:
            self.frames = self.kinect.getFrame()
            self.color = self.frames["color"]

            self.getLargestContour()
            self.getROIBounds()


            cv2.imshow("Color", cv2.resize(self.color, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()
            k = cv2.waitKey(10)

            if k == 27:
                self.getROIBounds()
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

    def getLargestContour(self):
        blur = cv2.medianBlur(self.color, 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, self.lowerThresh, self.upperThresh, cv2.ADAPTIVE_THRESH_MEAN_C)[1]

        cv2.imshow('thresh', cv2.resize(thresh, (int(1920 / 3), int(1080 / 3))))

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        contourAreas = [cv2.contourArea(c) for c in cnts]
        sortedAreas = sorted(zip(contourAreas, cnts), key = lambda x: x[0], reverse = True)

        # NOTE: Is there a way to improve this?
        # Find the nth largest contour [n-1][1]
        self.largestContour = sortedAreas[0][1]
        cv2.drawContours(self.color, self.largestContour, -1, (0,255,0), 10)


    def getDistance(self, x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

    def getROIPoints(self, x1, y1, x2, y2, p):
        d = self.getDistance(x1, y1, x2, y2)

        newx1 = x1 - int(d * p)
        x1 = 0 if newx1 < 0 else newx1

        newy1 = y1 - int(d * p)
        y1 = 0 if newy1 < 0 else newy1

        newx2 = x2 + int(d * p)
        x2 = width if newx2 > width else newx2

        newy2 = y2 + int(d * p)
        y2 = height if newy2 > height else newy2


        return (x1, y1, x2, y2)

    def getROIBounds(self):
        x, y, w, h = cv2.boundingRect(self.largestContour)
        return self.getROIPoints(x, y, x + w, y + h, 0.75)
