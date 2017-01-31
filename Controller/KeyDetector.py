import cv2
import numpy as np
import imutils

class KeyDetector:

    def __init__(self, kinect, bounds):
        self.kinect = kinect

        while True:
            self.frames = self.kinect.getFrame()
            color = self.frames["color"].asarray()
            self.bounded = color[bounds[1]: bounds[3], bounds[0]: bounds[2]]
            self.getKeyContours()

            cv2.imshow("Color", cv2.resize(self.bounded, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                break

    def getKeyContours(self):
        gray = cv2.cvtColor(self.bounded, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
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
