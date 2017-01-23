import cv2
import numpy as np
import imutils

class KeyDetector:

    def __init__(self):
        pass

    def receiveFrame(self, frame):
        self.data = frame.asarray()

    def getKeyContours(self, frame):
        gray = cv2.cvtColor(frame.asarray(), cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
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
        blur = cv2.medianBlur(frame.asarray(), 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
        

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        contours = []
        
        for idx, c in enumerate(cnts):
            M = cv2.moments(c)
            
            if all(x == 0 for x in M.values()):
                continue
            if int(M["m00"]) < 45000:
                continue
            contours.append(c)
        
        self.boundedConts = contours
        

        
    def transmitFrame(self):
        return self.data

    def transmitKeyContours(self):
        return self.contours
    
    def transmitBounds(self):
        return self.boundedConts
