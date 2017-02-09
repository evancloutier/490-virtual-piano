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
        
#                #color frame bounded by ROI bounds
        bNearXOffset, bNearYOffset, bFarXOffset, bFarYOffset = self.kinect.keyBounds
#        depthHeight, depthWidth = depthFrame.shape
#
#        #bNearXOFfset / origWidth = dX1 / dWidth
#        #dX1 = bNearXOffset * depthWidth / origWidth
#
#        widthScalingFactor = float(depthWidth) / origWidth
#        heightScalingFactor = float(depthHeight) / origHeight
#
#        dX1 = int((bNearXOffset + x1) * widthScalingFactor)
#        if dX1 * 0.9 > 0:
#            dX1 = int(dX1 * 0.9)
#
#        else:
#            dX1 = 0
#        dX2 = int((bNearXOffset + x2) * widthScalingFactor)
#        if dX2 * 1.1 < depthWidth:
#            dX2 = int(dX2 * 1.1)
#        else:
#            dX2 = depthWidth - 1
#        dY1 = int((bNearYOffset + y1) * heightScalingFactor)
#        if dY1 > depthHeight:
#            dY1 = 0
#        dY2 = int((bNearYOffset + y2) * heightScalingFactor)
#        if dY2 < 0:
#            dY2 = 0
        
        
        
        #create new finger points to return
        convertedFingerPoints = []
        
        yOffset, xOffset, _ = croppedColorFrame.shape
        
        #get scaling value first
        dY, dX = depthFrame.shape
        cY, cX, _ = self.kinect.originalColorFrame.shape
        
        print depthFrame.shape
        print self.kinect.originalColorFrame.shape
        
        yScalingFactor = float(dY) / cY
        xScalingFactor = float(dX) / cX
        print "yScalingFactor", yScalingFactor
        print "xScalingFactor", xScalingFactor
        
        for point in fingerPoints:
            print "point", point
            newX = (point[0] + bNearXOffset) * xScalingFactor
            newY = (point[1] + bNearYOffset) * yScalingFactor
            convertedFingerPoints.append((int(newX), int(newY)))
            print "new PointX", newX
            print "new Pointy", newY
            
        return convertedFingerPoints
