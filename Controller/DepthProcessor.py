import cv2
import numpy as np
import math
import os, sys
import imutils
import pdb

from sklearn.preprocessing import normalize

class DepthProcessor:
    def __init__(self, kinect):
        self.kinect = kinect

        while True:
            self.frames = self.kinect.getFrame()
            depth = self.frames["depth"]
            color = self.frames["color"]

            row, col = depth.shape
            norm = np.zeros((row, col))
            norm.fill(1000)
            normalized = depth / norm

            norm_gray = cv2.cvtColor(normalized, cv2.COLOR_BGR2GRAY)
            norm_color = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)

            cv2.imshow("Depth", depth / 4500.)
            cv2.imshow("Colorized Depth", norm_color)
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                break
