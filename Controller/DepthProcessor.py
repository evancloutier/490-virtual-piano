import cv2
import numpy as np
import math
import os, sys
import imutils
import pdb

class DepthProcessor:
    def __init__(self, kinect):
        self.kinect = kinect

    def processDepthFrame(self, depth):
        row, col = depth.shape

        # Create array to normalize depth values
        norm = np.zeros((row, col))
        norm.fill(1000)
        normDepth = depth / norm

        # Apply grayscale value to array
        for index, x in np.ndenumerate(normDepth):
            if math.isnan(x):
                continue
            else:
                updated = self.getGrayscaleValue(1, 0, x)
                normDepth.itemset(index, updated)

        # Cast to np.uint8
        grayDepth = normDepth.astype(np.uint8, copy = True)

        # Convert grayscale value to RGB
        colorDepth = cv2.cvtColor(grayDepth, cv2.COLOR_GRAY2RGB)

        # Apply color map to RGB array
        colorMap = cv2.applyColorMap(colorDepth, cv2.COLORMAP_WINTER)
        

        # Return it to display
        return colorMap

    def getGrayscaleValue(self, highBound, lowBound, value):
        if math.isnan(value):
            return 0
        else:
            return int(((255) * (value - lowBound)) / (highBound - lowBound) + lowBound)

    def generateRGBList(self, value):
        rgb = value * 0x00010101
        
    def convertColorFingerPoints(self, fingerPoints, depthFrame, croppedColorFrame):
        
        #color frame bounded by ROI bounds
        bNearXOffset, bNearYOffset, bFarXOffset, bFarYOffset = self.kinect.keyBounds
        
        #get shape of depth frame
        dY, dX = depthFrame.shape
        
        cY, cX, _ = self.kinect.originalColorFrame.shape
        
        #create new finger points to return
        convertedFingerPoints = []
        
        xM1 = 278 #Manually calibrated difference between depth range and color range
        xM2 = 1795
        
        
        yScalingFactor = float(dY) / cY
        if fingerPoints is not None:
            for point in fingerPoints:
                fX = point[0]
                fY = point[1]
                fX = fX + (bNearXOffset - xM1)
                depthPointX = (float(fX) * dX)/(cX - xM1 - (cX - xM2) )
                depthPointY = (fY + bNearYOffset) * yScalingFactor
                convertedFingerPoints.append([int(depthPointX), int(depthPointY)])
                
            
        return convertedFingerPoints
