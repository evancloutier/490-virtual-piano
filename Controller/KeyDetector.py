import cv2
import numpy as np
import imutils
import FrameType

ft = FrameType.FrameType()

class KeyDetector:

    def __init__(self, kinect):
        self.kinect = kinect

        # Note this while loop should eventually be moved into Main.py
        while True:
            self.frame = self.kinect.getFrame(ft.Color)
            self.getKeyContours()

            cv2.imshow("Color", cv2.resize(self.frame, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                break

    def getKeyContours(self):
        # img = cv2.imread("lenna.png")
        # crop_img = img[200:400, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400
        # # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        # cv2.imshow("cropped", crop_img)
        # cv2.waitKey(0)

        # Width: 1920, Height: 1080

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
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
