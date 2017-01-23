import cv2
import numpy as np
import imutils

class KeyDetector:

    def __init__(self, kinect=None):
        self.kinect = kinect
        self.xoffset = 10
        self.yoffset = 100

    def receiveFrame(self, frame):
        self.data = frame.asarray()

    def getKeyContours(self, frame):
        gray = cv2.cvtColor(frame.asarray(), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        contours = []

        for idx, c in enumerate(cnts):
            M = cv2.moments(c)

            # Eliminate the contour if the moment is zero
            if all(x == 0 for x in M.values()):
                continue

            # Eliminate smaller contours based on area
            if int(M["m00"]) < 3000:
                continue
            else:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                contour = [c, cX, cY]
                contours.append(contour)
        contours.sort(key = lambda x: x[1])

        self.contours = contours

    def getOutsideContours(self, frame):
        blur = cv2.medianBlur(frame, 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]


        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        contours = []

        maxSize = 0
        for idx, c in enumerate(cnts):
            M = cv2.moments(c)

            if not all(x == 0 for x in M.values()):
                if int(M["m00"]) > maxSize:
                    maxSize = int(M["m00"])
                    if len(contours) > 0:
                        contours.pop(-1)
                    contours.append(c)


        self.boundedConts = contours


    def getBounds(self):

        minusBool = 1
        x = None
        y = None
        w = None
        h = None
        while True:

            frame = self.kinect.getFrame(self.kinect.rgbSharedMem)

            self.getOutsideContours(frame)

            for contour in self.boundedConts:
                #epsilon marks accuracy of square
                epsilon = 0.1*cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                x, y, w, h = cv2.boundingRect(approx)

                cv2.rectangle(frame, (x, y), (x + w + self.xoffset, y + h + self.yoffset), (255, 0, 0), 2)

            k = cv2.waitKey(10)
            if k == ord('-'):
                print("toggled subtraction mode")
                minusBool = -1 * minusBool
            if k == ord('x'):
                self.xoffset += 5 * minusBool
            if k == ord('y'):
                self.yoffset += 5 * minusBool
            if k == 27:
                cv2.destroyAllWindows()
                break

            cv2.imshow('bounding rectange', frame)

        return (x - self.xoffset, x + w + self.xoffset, y)


    def transmitFrame(self):
        return self.data

    def transmitKeyContours(self):
        return self.contours
