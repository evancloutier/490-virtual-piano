import cv2
import math
import numpy as np
import imutils
import FrameType

ft = FrameType.FrameType()

class BoundsDetector:

    def __init__(self, kinect):
        self.kinect = kinect

        while True:
            self.frame = self.kinect.getFrame(ft.Color)
            self.getLargestContour()

            cv2.imshow("Color", cv2.resize(self.frame, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                # Get the ROI bounds
                self.getROIBounds()
                cv2.destroyAllWindows()
                break

    def getLargestContour(self):
        blur = cv2.medianBlur(self.frame, 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        contourAreas = [cv2.contourArea(c) for c in cnts]
        sortedAreas = sorted(zip(contourAreas, cnts), key = lambda x: x[0], reverse = True)

        # Find the nth largest contour [n-1][2n-1]
        self.largestContour = sortedAreas[0][1]

    def getDistance(self, x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

    def getROIPoints(self, x1, y1, x2, y2, p):
        d = self.getDistance(x1, y1, x2, y2)
        x1 = x1 - int(d * p)
        y1 = y1 - int(d * p)
        x2 = x2 + int(d * p)
        y2 = y2 + int(d * p)
        return (x1, y1, x2, y2)

    def getROIBounds(self):
        x, y, w, h = cv2.boundingRect(self.largestContour)
        return self.getROIPoints(x, y, x + w, y + h, 0.5)
