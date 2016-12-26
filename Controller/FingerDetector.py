import cv2
import cv2.cv as cv
import time
import numpy as np
import math
import os, sys
import pdb


width = 512
height = 424
blackImg = np.zeros((424,512,3), np.uint8)

class FingerDetector:
    def __init__(self, bottomLine, blurPixelSize, threshVal, bothHands=True, kinect=None):
        self.vidSrc = cv2.VideoCapture(0)
        self.background = cv2.BackgroundSubtractorMOG2()
        self.buildBackgroundModel(kinect)
        self.blurPixelSize = blurPixelSize
        self.bothHands = bothHands
        self.bottomLine = bottomLine
        self.threshVal = threshVal

    def adjustParams(self, k):
        if k == ord('q') and self.blurPixelSize < 30:
            self.blurPixelSize += 2
            print "blur size += 2 ", self.blurPixelSize
        elif k == ord('w') and self.blurPixelSize > 2:
            self.blurPixelSize -= 2
            print "blur size -= 2 ", self.blurPixelSize
        elif k == ord('a') and self.threshVal < 251:
            self.threshVal += 5
            print "threshold += 5 ", self.threshVal
        elif k == ord('s') and self.threshVal > 6:
            self.threshVal -= 5
            print "threshold -= 5 ", self.threshVal

    def continuousFingers(self):
        while True:
            #frame = self.getFrame()
            fingerPoints, fingerImage = self.getFingerPositions()
            k = cv2.waitKey(10)
            if k == 27:
                break
            else:
                self.adjustParams(k)
            cv2.imshow('a', fingerImage)

    def getFingerPositions(self, frame=None):
        if frame is None:
            frame = self.getFrame()

        diff = self.background.apply(frame)
        diff = self.filterBottom(diff, self.bottomLine)
        blackImgCopy = self.getBackgroundCopy()
        self.drawBottomLine(blackImgCopy, self.bottomLine)
        blur = self.blurFrame(diff, self.blurPixelSize)
        thresh = self.thresholdFrame(blur, self.threshVal)

        leftHand, rightHand = self.getLargestShapes(thresh, self.bothHands)

        numHands = 1
        if self.bothHands:
            numHands = 2
            leftHand, rightHand = self.getHandSides(leftHand, rightHand)


        hand = leftHand
        isLeftHand = True
        fingerPoints = []

        for i in range(numHands):

            self.drawShape(blackImgCopy, hand)

            centerOfHand = self.getCenterOfHand(hand)
            self.drawCenterOfHand(blackImgCopy, centerOfHand)

            hullWithPoints, hullWithoutPoints = self.getConvexHull(hand)
            self.drawConvexHull(blackImgCopy, hullWithoutPoints)

            topFingers = self.getFingerPointsFromHull(hullWithoutPoints, centerOfHand)
            if topFingers is not None:
                fingerPoints.extend(topFingers)

            defects = self.getConvexDefects(hand, hullWithPoints)
            #fingerDefects = self.getFingerConvexDefects(blackImgCopy, defects, hand, centerOfHand)

            self.drawDefects(blackImgCopy, centerOfHand, defects, hand)

            thumbPoint = self.getThumbPoint(hand, defects, centerOfHand, isLeftHand)

            if fingerPoints is not None and thumbPoint is not None:
                fingerPoints.append(thumbPoint)

            fingerPoints = self.checkForOverlappingPoints(fingerPoints)

            self.drawFingerPoints(blackImgCopy, fingerPoints)

            #second iteration
            hand = rightHand
            isLeftHand = False

        return (fingerPoints, blackImgCopy)


    '''frame/ diffing functions'''
    def getFrame(self):
        ret, frame = self.vidSrc.read()
        return frame


    def buildBackgroundModel(self, kinect=None):
        print "Hit esc to exit background mode"
        while True:
                frame = None
                if kinect is None:
                    frame = self.getFrame()
                else:
                    frame = kinect.getFrame(kinect.rgbSharedMem)
                fgmask = self.background.apply(frame, learningRate=0.1)
                cv2.imshow('Foreground', fgmask)
                cv2.imshow('Original', frame)
                if cv2.waitKey(10) == 27:
                    break


    def getBackgroundCopy(self):
        return blackImg.copy()


    '''bluring / thresholding functions'''
    def blurFrame(self, frame, blurPixelSize):
        blur = cv2.medianBlur(frame, blurPixelSize)
        return blur


    def thresholdFrame(self, frame, threshVal):
        maxVal = 255
        ret, threshFrame = cv2.threshold(frame, threshVal, maxVal, cv2.THRESH_BINARY)
        return threshFrame


    '''shape functions'''
    def getLargestShapes(self, frame, bothHands=False):
        contours, contourHeirarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        maxContourSize = 0
        largestContour = []
        secondLargestContour = []
        for contour in contours:
            if len(contour) > maxContourSize:
                maxContourSize = len(contour)
                secondLargestContour = largestContour
                largestContour = contour

        if bothHands:
            return (largestContour, secondLargestContour)
        return (largestContour, None)


    def getConvexHull(self, contour):
        hull = None
        hull1 = None
        if contour is not None and len(contour) > 0:
            hull = cv2.convexHull(contour, returnPoints=False)
            hull1 = cv2.convexHull(contour)
        return hull, hull1


    def filterBottom(self, diff, bottomLine):
        for idx in range(bottomLine, len(diff)):
            row = diff[idx]
            for elemIdx in range(len(row)):
                row[elemIdx] = 0
        return diff


    def getConvexDefects(self, contour, hull):
        defects = None
        if hull is not None and len(hull) > 3 and contour is not None:
            defects = cv2.convexityDefects(contour, hull)
        return defects

    def checkForOverlappingPoints(self, points):
        if points is None:
            return None

        minDist = 20
        hasChanged = True

        while hasChanged:
            hasChanged = False
            for idx1 in range(len(points)):
                for idx2 in range(len(points)):
                    if idx1 != idx2 and hasChanged is False:
                        dist = math.sqrt( math.pow(points[idx1][0] - points[idx2][0], 2) + math.pow(points[idx1][1] - points[idx2][1], 2))
                        if dist <= minDist:
                            del points[idx1]
                            hasChanged = True

        return points


    '''hand geometry functions'''
    def getCenterOfHand(self, contour):
        centerOfHand = None
        if contour is not None and len(contour) > 0:
            handMoments = cv2.moments(contour, binaryImage=1)
            if handMoments['m00'] != 0:
                centerX = int(handMoments['m10']/handMoments['m00'])
                centerY = int(handMoments['m01']/handMoments['m00'])
                centerY -= centerY*0.30
                centerOfHand = (centerX, int(centerY))
        return centerOfHand


    def getFingerPointsFromHull(self, hull, centerOfHand):
        centers = None
        if hull is not None and len(hull) > 3:
            #k means clustering
            k = 4
            filteredCenters = None
            kmeansHull = []
            for elem in hull:
                if elem[0][1] <= centerOfHand[1]:
                    kmeansHull.append([np.float32(elem[0][0]), np.float32(elem[0][1])])

            kmeansHull = np.asarray(kmeansHull)

            if len(kmeansHull) >= k:
                maxIters = 100
                criteria = (cv2.TERM_CRITERIA_EPS, 10, 0.1)
                retval, bestLabels, centers = cv2.kmeans(kmeansHull, k, criteria, maxIters, cv2.KMEANS_PP_CENTERS)
                centers = centers.tolist()
                centers = [[int(x), int(y)] for x,y in centers]

        return centers

    #not really that useful
    def getFingerConvexDefects(self, img, defects, contour, center):
        if defects is None:
            return None
        defects = self.getLongestDefects(defects, 4)
        filteredDefects = []
        for defect in defects:
            s, e, f, d = defect[0]
            start = tuple(contour[s][0])
            farthest = tuple(contour[f][0])
            end = tuple(contour[e][0])

            if start[1] < center[1] and farthest[1] < center[1] and end[1] < center[1]:
                filteredDefects.append(defect)


    def getLongestDefects(self, defects, n, clockwise=True):
        largestDefects = []
        usedIdxs = set()

        for i in range(n):
            maxDist = float("-inf")
            maxIdx = -1
            for idx, defect in enumerate(defects):
                distance = defect[0][3]
                if distance > maxDist and idx not in usedIdxs:
                    maxDist = distance
                    maxIdx = idx
            usedIdxs.add(maxIdx)

        usedIdxs = sorted(list(usedIdxs), reverse=clockwise)

        for idx in usedIdxs:
            largestDefects.append(defects[idx])

        return largestDefects


    def getThumbPoint(self, contour, defects, centerOfHand, leftHand=True):
        if defects is None or contour is None or centerOfHand is None:
            return None
        maxDistance = 0
        longestDefect = None
        for defect in defects:
            s, e, f, distance = defect[0]
            start = tuple(contour[s][0])
            farthest = tuple(contour[f][0])
            end = tuple(contour[e][0])

            if distance > maxDistance:
                if leftHand:
                    #if thumb is on right hand side
                    if start[0] > centerOfHand[0] and farthest[0] > centerOfHand[0] and end[0] > centerOfHand[0]:
                        #if start is below and end is above
                        if start[1] > centerOfHand[1] and end[1] < centerOfHand[1]:
                            maxDistance = distance
                            longestDefect = defect.copy()
                if leftHand is False:
                    #if thumb on left hand side
                    if start[0] < centerOfHand[0] and farthest[0] < centerOfHand[0] and end[0] < centerOfHand[0]:
                        if end[1] > centerOfHand[1] and start[1] < centerOfHand[1]:
                            maxDistance = distance
                            longestDefect = defect.copy()

        if longestDefect is None:
            return None

        s, e, f, d = longestDefect[0]
        if leftHand:
            thumbPoint = ((contour[s][0][0] + contour[f][0][0]) / 2, (contour[s][0][1] + contour[f][0][1]) / 2)
        elif leftHand is False:
            thumbPoint = ((contour[e][0][0] + contour[f][0][0]) / 2, (contour[e][0][1] + contour[f][0][1]) / 2)
        return thumbPoint


    def getHandSides(self, hand1, hand2):
        if hand1 is None and hand2 is None:
            return (None, None)
        elif hand1 is None:
            return (hand1, None)
        elif hand2 is None:
            return (hand2, None)
        hand1Center = self.getCenterOfHand(hand1)
        hand2Center = self.getCenterOfHand(hand2)

        leftHand = hand1
        rightHand = hand2

        if hand1Center is not None and hand2Center is not None and hand1Center[0] > hand2Center[0]:
            leftHand = hand2
            rightHand = hand1

        return (leftHand, rightHand)


    '''drawing functions'''
    def drawShape(self, frame, contour):
        if contour is not None and len(contour) >= 1:
            cv2.drawContours(frame, contour, -1, (255,255,255), thickness=5)
            cv2.fillPoly(frame, pts=[contour], color=(255,255,255))

    def drawBottomLine(self, frame, bottomLine):
        start = (0, bottomLine)
        end = (width, bottomLine)
        cv2.line(frame, start, end, (0,255,255), thickness=3)

    def drawConvexHull(self, frame, contour):
        convexHull = None
        if contour is not None:
            convexHull = cv2.convexHull(contour)
        if convexHull is not None and len(convexHull) > 2:
            for idx in range(len(convexHull) - 1):
                cv2.line(frame, tuple(convexHull[idx][0]), tuple(convexHull[idx + 1][0]), (0,255,255), thickness=10)
            cv2.line(frame, tuple(convexHull[0][0]), tuple(convexHull[-1][0]), (0, 255, 255), thickness= 10)

    def drawCenterOfHand(self, frame, centerOfHand):
        if centerOfHand is not None:
            cv2.circle(frame, centerOfHand, 5, (255, 255, 0), thickness=5)

    def drawFingerPoints(self, frame, fingerPoints):
        if fingerPoints is not None:
            for fingerCoord in fingerPoints:
                if fingerCoord is not None:
                    if type(fingerCoord) is not tuple:
                        fingerCoord = tuple(fingerCoord)
                    cv2.circle(frame, fingerCoord, 5, (255, 0, 255), thickness=5)


    def drawDefects(self, frame, centerOfHand, defects, contour):
        if centerOfHand is not None and defects is not None and contour is not None:
            for defect in defects:
                s, e, f, d = defect[0]
                start = tuple(contour[s][0])
                farthest = tuple(contour[f][0])
                end = tuple(contour[e][0])
                #if start[0] > centerOfHand[0] and farthest[0] > centerOfHand[0] and end[0] > centerOfHand[0]:
                cv2.line(frame, start, farthest, (0,255,0), thickness=5)
                cv2.line(frame, farthest, end, (0,255,0), thickness=5)



#fingerDetector = FingerDetector(300, 27, 159, False)
#fingerDetector.continuousFingers()
