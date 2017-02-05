import cv2
import numpy as np
import math
import os, sys
import imutils
import pdb

class DepthProcessor:
    def __init__(self, kinect):
        self.kinect = kinect

        # Grab a single frame
        self.frames = self.kinect.getFrame()
        depth = self.frames["depth"]

        # Set the depth value to be in metres (between 0-1)
        row, col = depth.shape
        reg = np.zeros((row, col))
        reg.fill(1000)
        newDepth = depth / reg

        # Normalize the values within the numpy array
        for index, x in np.ndenumerate(newDepth):
            if math.isnan(x):
                continue
            else:
                updated = self.normalizeDepthValue(1, 0, x)
                newDepth.itemset(index, updated)

        # Create a copy of the array with data type np.uint8
        normDepth = newDepth.astype(np.uint8, copy = True)

        # Convert the depth to RGB
        depthColor = cv2.cvtColor(normDepth, cv2.COLOR_GRAY2RGB)
        colorMap = cv2.applyColorMap(depthColor, cv2.COLORMAP_WINTER)

        while True:
            cv2.imshow("Depth", depth / 4500.)
            cv2.imshow("Depth Color Map", colorMap)

            k = cv2.waitKey(10)

            if k == 27:
                break

    def normalizeDepthValue(self, highBound, lowBound, value):
        if math.isnan(value):
            return 0
        else:
            return int(((255) * (value - lowBound)) / (highBound - lowBound) + lowBound)

    def generateRGBList(self, value):
        rgb = value * 0x00010101
