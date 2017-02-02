import cv2
import time
import numpy as np
import math
import os, sys
import imutils
import pdb
from skimage.morphology import skeletonize
from matplotlib import pyplot as plt

width = 1920
height = 1080

blackImg = np.zeros((height,width,3), np.uint8)

class FingerDetector:
    def __init__(self, blurPixelSize, threshVal, bothHands=True, kinect=None):
        self.vidSrc = cv2.VideoCapture(0)
        self.blurPixelSize = blurPixelSize
        self.bothHands = bothHands
        self.threshVal = threshVal
        self.hist = None
        self.hand = None
        self.handWidth = 1
        self.fingerPoints = None

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
            frame = self.getFrame()
            fingerPoints, fingerImage = self.getFingerPositions(frame)
            k = cv2.waitKey(10)
            if k == 27:
                break
            else:
                self.adjustParams(k)
            cv2.imshow('a', fingerImage)

    def convertPointsToNumpy(self, points):
        for idx1 in range(len(points)):
            points[idx1] = list(points[idx1])
            for idx2 in range(2):
                points[idx1][idx2] = np.float32(points[idx1][idx2])
            points[idx1] = [points[idx1]]
        p0 = np.asarray(points)
        return p0

    #http://www.benmeline.com/finger-tracking-with-opencv-and-python/
    def getSkinSamples(self, frame, sampleRadius=5):
        sampleWidth = 100
        sampleHeight = 200
        numSamples = 9

        startingWidth = (width - sampleWidth) / 2
        startingHeight = (height - sampleHeight) / 2

        numCols = int(math.sqrt(numSamples))
        numRows = int(math.sqrt(numSamples))

        colWidth = sampleWidth / numCols
        rowHeight = sampleHeight / numRows

        currCol = 0
        currRow = 0
        currWidth = 0
        currHeight = 0

        sampleCenters = []

        for sample in range(numSamples):
            currRow = sample / numRows
            currCol = sample % numCols

            currHeight = startingHeight + (currRow * rowHeight)
            currWidth = startingWidth + (currCol * colWidth)

            self.drawCenterOfHand(frame, (currWidth, currHeight), color=(0,255,0))
            sampleCenters.append([currWidth, currHeight])


        return sampleCenters

    def getHandColors(self, frame, samplePoints, sampleRadius=5):
        frame = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = np.zeros(frame.shape[:2], np.uint8)

        idx = 0
        for x,y in samplePoints:
            for xIdx in range(x - sampleRadius, x + sampleRadius):
                for yIdx in range(y - sampleRadius, y + sampleRadius):
                    mask[yIdx][xIdx] = 255
            idx += 1
        maskedImage = cv2.bitwise_and(frame, frame, mask=mask)

        color = ('b','g','r')
        hist = cv2.calcHist([hsv], [0], mask, [256], [0,256])
        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

        return hist

    def buildSkinColorHistogram(self, kinect):
        handHistogram = None
        while True:
            frame = kinect.getFrame()["color"]
            originalFrame = frame.copy()
            samplePoints = self.getSkinSamples(frame)

            cv2.imshow('skin color', cv2.resize(frame, (int(1920 / 3), int(1080 / 3))))
            kinect.releaseFrame()

            k = cv2.waitKey(10)
            if k == 27:
                self.hist = self.getHandColors(originalFrame, samplePoints)
                cv2.destroyAllWindows()
                break

    def applyHistogram(self, frame):
        frame = frame.copy()
        blackImgCopy = self.getBackgroundCopy(len(frame), len(frame[0]))
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        filteredIm = cv2.calcBackProject([hsv], [0], self.hist, [0,180,0,256], 1)

        cpy = filteredIm.copy()

        filteredIm = self.blurFrame(filteredIm, self.blurPixelSize)
        hand = self.getLargestShapes(filteredIm)[0]
        filteredIm = self.drawShape(blackImgCopy, hand)
        self.hand = hand

        return (blackImgCopy, cpy)

    def getFarPoint(self, cnt, centerOfHand):
        maxDist = self.distanceBetweenPoints(cnt[0][0], centerOfHand)
        maxPoint = cnt[0][0]
        for idx in range(1, len(cnt)):
            dist = self.distanceBetweenPoints(cnt[idx][0], centerOfHand)
            if dist > maxDist:
                maxDist = dist
                maxPoint = cnt[idx][0]
        return maxPoint

    def getClosestPoint(self, cnt, centerOfHand):
        minDist = self.distanceBetweenPoints(cnt[0][0], centerOfHand)
        minPoint = cnt[0][0]
        for idx in range(1, len(cnt)):
            dist = self.distanceBetweenPoints(cnt[idx][0], centerOfHand)
            if dist < minDist:
                minDist = dist
                minPoint = cnt[idx][0]
        return minPoint

    def getExtremePoints(self, cnt, centerOfHand):
        closePoint = self.getClosestPoint(cnt, centerOfHand)
        farPoint = self.getFarPoint(cnt, centerOfHand)

        if closePoint[1] > farPoint[1]:
            return None
        return farPoint

    def getFingerPositions(self, binaryIm):
        centerOfHand = self.getCenterOfHand(self.hand)
        binaryIm = self.skeletonizeHand(binaryIm, centerOfHand)

        a = binaryIm.copy()

        blackImgCopy = blackImg.copy()

        otsuRet, otsuThresh = cv2.threshold(binaryIm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cnts = cv2.findContours(otsuThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        farPoints = []
        for cnt in cnts:
            farPoint = self.getExtremePoints(cnt, centerOfHand)
            if farPoint is not None:
                farPoints.append(farPoint)
            cv2.drawContours(blackImgCopy, [cnt], -1, (255, 255, 255), 2)


        for point in farPoints:
            cv2.circle(blackImgCopy, (point[0], point[1]), 4, color=(0,255,0), thickness=3)

        return (a, farPoints)
        #return (blackImgCopy, farPoints)


    #http://opencvpython.blogspot.ca/2012/05/skeletonization-using-opencv-python.html
    #getFingerPositions
    def skeletonizeHand(self, binaryIm, centerOfHand):
        binaryIm = cv2.cvtColor(binaryIm, cv2.COLOR_RGB2GRAY)
        binaryImCopy = binaryIm.copy()

        binaryIm[binaryIm == 255] = 1
        skeleton = skeletonize(binaryIm)

        binaryIm[skeleton == 1] = 255

        kernel = np.ones((5, 5))
        binaryIm = cv2.dilate(binaryIm, kernel, iterations=1)

        self.removeCenterOfHand(binaryImCopy, binaryIm, centerOfHand, self.hand)

        return binaryIm

    '''frame/ machine learning functions'''

    def getFrame(self):
        ret, frame = self.vidSrc.read()
        return frame


    def buildBackgroundModel(self, kinect):
        print "Hit esc to exit background mode"
        cv2.ocl.setUseOpenCL(False)
        while True:
                frame = kinect.getFrame()["color"]
                fgmask = self.background.apply(frame)
                cv2.imshow('Foreground', fgmask)
                cv2.imshow('Original', frame)
                if cv2.waitKey(10) == ord('z'):
                    cv2.destroyAllWindows()
                    break


    def getBackgroundCopy(self, height, width):
        img = np.zeros((height,width,3), np.uint8)
        return img


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
        _, contours, contourHeirarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
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


    def filterOutside(self, diff):
        for xIdx in range(0, width):
            for yIdx in range(0, height):
                if xIdx < self.leftLineX or xIdx > self.rightLineX or yIdx < self.bottomLineY:
                    diff[yIdx][xIdx] = 0
        return diff


    def getConvexDefects(self, contour, hull):
        defects = None
        if hull is not None and len(hull) > 3 and contour is not None:
            defects = cv2.convexityDefects(contour, hull)
        return defects

    def checkForOverlappingPoints(self, points):
        if points is None:
            return None

        minDist = 5
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
    def distanceBetweenPoints(self, point1, point2):
        if point1 is None or point2 is None:
            return float("inf")
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def getCenterOfHand(self, contour):
        centerOfHand = None
        if contour is not None and len(contour) > 0:
            handMoments = cv2.moments(contour, binaryImage=1)
            if handMoments['m00'] != 0:
                centerX = int(handMoments['m10']/handMoments['m00'])
                centerY = int(handMoments['m01']/handMoments['m00'])
                #centerY -= centerY * 0.1
                centerOfHand = (centerX, int(centerY))
        return centerOfHand


    def getFingerPointsFromHull(self, hull, centerOfHand):
        centers = None
        if hull is not None and len(hull) > 3 and centerOfHand is not None:
            #k means clustering
            k = 4
            filteredCenters = None
            kmeansHull = []
            for elem in hull:
                if elem[0][1] >= centerOfHand[1]:
                    kmeansHull.append([np.float32(elem[0][0]), np.float32(elem[0][1])])

            kmeansHull = np.asarray(kmeansHull)

            if len(kmeansHull) >= k:
                maxIters = 100
                criteria = (cv2.TERM_CRITERIA_EPS, 10, 0.1)
                retval, bestLabels, centers = cv2.kmeans(kmeansHull, k, None, criteria, maxIters, cv2.KMEANS_PP_CENTERS)
                centers = centers.tolist()
                centers = [[int(x), int(y)] for x,y in centers]

        return centers

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

            if start is not None and center is not None and end is not None:
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

    '''drawing functions'''
    def drawShape(self, frame, contour, shapeColor=(255,255,255)):
        if contour is not None and len(contour) >= 1:
            cv2.fillPoly(frame, pts=[contour], color=shapeColor)

    def drawConvexHull(self, frame, contour):
        convexHull = None
        if contour is not None:
            convexHull = cv2.convexHull(contour)
        if convexHull is not None and len(convexHull) > 2:
            for idx in range(len(convexHull) - 1):
                cv2.line(frame, tuple(convexHull[idx][0]), tuple(convexHull[idx + 1][0]), (0,255,255), thickness=5)
            cv2.line(frame, tuple(convexHull[0][0]), tuple(convexHull[-1][0]), (0, 255, 255), thickness= 5)

    def drawCenterOfHand(self, frame, centerOfHand, color=(255,255,0), width=3, thickness=2):
        if centerOfHand is not None:
            if type(centerOfHand) == np.ndarray:
                centerOfHand = (centerOfHand[0][0], centerOfHand[0][1])
            cv2.circle(frame, centerOfHand, width, color, thickness)
            #cv2.circle(frame, centerOfHand, 5, 100, thickness=5)

    def drawEllipse(self, frame, center, width):
        box = (int(center[0]), int(center[1]), int(width), int(width/2), 0)
        #cv2.ellipse(frame, box, color=(0,0,0), thickness=-1)
        cv2.ellipse(frame, (center[0],center[1]), (width, width/2), 0, 0, 180, (0,0,0), 2)

    def removeCenterOfHand(self, frame, frameToDraw, centerOfHand, contour):
        if centerOfHand is not None and contour is not None:
            handWidth = 0
            centerX = centerOfHand[0]
            centerY = centerOfHand[1]
            for i in range(centerX, len(frame)):
                if frame[centerY][i] == 255:#set([255, 255, 255]):
                    handWidth += 1
            for i in range(centerX, 0, -1):
                if frame[centerY][i] == 255:#set([255,255,255]):
                    if abs(centerX - i) > handWidth:
                        handWidth += 1
            handWidth += 1
            self.handWidth = handWidth
            self.drawCenterOfHand(frameToDraw, centerOfHand, color=0, width=2*handWidth/3, thickness=-1)

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
