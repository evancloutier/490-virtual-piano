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
        self.frameCounter = 0

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
        
        index = None
        
        keyDict = {("C1":(0, False)),("Db1":(1, False)),("D1":(2, False))
                   ,("Eb1":(3, False)),("E1":(4, False)),("F1":(5, False))
                   ,("Gb1":(6, False)),("G1":(7, False)),("Ab1":(8, False))
                   ,("A1":(9, False)),("Bb1":(10, False)),("B1":(11, False))}
        
        if keysBeingPressed is not None:
            for key in keysBeingPressed:
                index, isPressed = keyDict.get(key, None)
                keyDict[key] = index, True
                
            

            for key, value in keyDict:
                if self.frameCounter >= 20:
                    self.avgKeyMat[value[0]].popLeft()
                if value[1] == True:
                    self.avgKeyMat[value[0]].append(1)
                elif value[1] == False:
                    self.avgKegMat[[value[0]]].append(0)
                

        print self.avgKeyMat
        self.frameCounter = self.frameCounter + 1

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

            if depthDifference < 20:
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
