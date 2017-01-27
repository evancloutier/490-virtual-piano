import cv2
import numpy as np
import imutils
import FrameType

ft = FrameType.FrameType()

class BoundsDetector:

    def __init__(self, kinect):
        self.kinect = kinect

        while True:
            self.frame = self.kinect.getFrame(ft.Color)
            self.getBoundingRectangle()

            cv2.imshow("Color", cv2.resize(self.frame, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                break

    def getBoundingRectangle(self):
        blur = cv2.medianBlur(self.frame, 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 251, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
        cv2.imshow("Blur", cv2.resize(blur, (int(1920 / 3), int(1080 / 3))))

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        contourAreas = [cv2.contourArea(c) for c in cnts]
        sortedAreas = sorted(zip(contourAreas, cnts), key = lambda x: x[0], reverse = True)
        largestContour = sortedAreas[0][1]

        x, y, w, h = cv2.boundingRect(largestContour)


        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
