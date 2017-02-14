import cv2
import numpy as np
import math
import os, sys
import imutils
import pdb

class DepthProcessor:
    def __init__(self, kinect):
        self.kinect = kinect
        self.sumDepthValues = np.zeros((424, 512))
        self.depthValues = None
        self.avgKeyMat = self.buildAverageKeyMat()
        self.frameCounter = 0

    def buildAverageKeyMat(self):
        keys = {"C1": [0],"Db1": [0],"D1": [0]
               ,"Eb1": [0],"E1": [0],"F1": [0]
               ,"Gb1": [0],"G1": [0],"Ab1": [0]
               ,"A1": [0],"Bb1": [0],"B1": [0]
               ,"C2": [0],"Db2": [0],"D2": [0]
               ,"Eb2": [0],"E2": [0],"F2": [0]
               ,"Gb2": [0],"G2": [0],"Ab2": [0]
               ,"A2": [0],"Bb2": [0],"B2": [0]}
        return keys

    def initializeDepthMap(self, depth, counter):
        row, col = depth.shape


        # Copying our depth values
        for index, x in np.ndenumerate(depth):
            if math.isnan(x):
                continue
            else:
                if counter == 0:
                    self.sumDepthValues.itemset(index, x)
                else:
                    prevDepth = self.sumDepthValues.item(index)
                    self.sumDepthValues.itemset(index, (x + prevDepth))

    def calculateNotesMatrix(self, keysBeingPressed):

        numFramesToConsider = 4
        threshVal = 2
        if len(self.avgKeyMat["C1"]) >= numFramesToConsider:
            for key in self.avgKeyMat:
                self.avgKeyMat[key].pop(0)

        if keysBeingPressed is not None:
            for key in self.avgKeyMat:
                self.avgKeyMat[key].append(0)
                if key in keysBeingPressed:
                    self.avgKeyMat[key][-1] = 1

        notes = []
        for key in self.avgKeyMat:
            if sum(self.avgKeyMat[key]) > threshVal:
                notes.append(key)
        return notes


    def checkFingerPoints(self, depthFrame, keysBeingHovered):
        #so we loop through each of points in keysBeingHovered
        #convert that point to depth point
        #check that depth point value with self.depthValues point

        keysBeingPressed = []

        for key in keysBeingHovered:
            colorPoint = keysBeingHovered[key]
            #now convert point
            depthPointX, depthPointY = self.convertColorFingerPoint(colorPoint, depthFrame)

            #draw point to show it works
            cv2.circle(depthFrame, (depthPointX, depthPointY), 4, color=(255,255,0), thickness=3)

            #now use that depthPoint to determine depth at that point
            depthDifference = self.depthValues.item(depthPointY, depthPointX) - depthFrame.item(depthPointY, depthPointX)
            print depthDifference

            if depthDifference < 15:
                keysBeingPressed.append(key)

        return keysBeingPressed



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

    def convertColorFingerPoint(self, fingerPoint, depthFrame):

        #color frame bounded by ROI bounds
        bNearXOffset, bNearYOffset, bFarXOffset, bFarYOffset = self.kinect.keyBounds

        #get shape of depth frame
        dY, dX = depthFrame.shape

        cY, cX, _ = self.kinect.originalColorFrame.shape

        xM1 = 278 #Manually calibrated difference between depth range and color range
        xM2 = 1795

        yScalingFactor = float(dY) / cY
        if fingerPoint is not None:
            fX = fingerPoint[0]
            fY = fingerPoint[1]
            fX = fX + (bNearXOffset - xM1)
            depthPointX = (float(fX) * dX)/(cX - xM1 - (cX - xM2) )
            depthPointY = (fY + bNearYOffset) * yScalingFactor


        return int(depthPointX), int(depthPointY)
