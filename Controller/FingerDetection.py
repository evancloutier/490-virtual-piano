import cv2
import cv2.cv as cv
import time
import numpy as np
import os, sys
import pdb

width = 512
height = 424

def drawFingerCoords(img, fingerCoords):
    if fingerCoords is None:
        return
    for fingerCoord in fingerCoords:
        if type(fingerCoord) is not tuple:
            fingerCoord = tuple(fingerCoord)
        cv2.circle(img, fingerCoord, 5, (255, 0, 255), thickness=5)

def averageDefects(defect1, defect2, contour):

    s1, e1, f1, d1 = defect1
    s2, e2, f2, d2 = defect2

    start = contour[s1][0]
    end = contour[e2][0]

    newX = (start[0] + end[0])/2
    newY = (start[1] + end[1])/2

    return (newX, newY)


def getFingerPointsFromDefect(longestDefects, contour):
    largestIdx = len(longestDefects) - 1
    fingerPoints = []

    for idx, defect in enumerate(longestDefects):
        s, e, f, d = defect[0]
        if idx == 0:
            fingerPoints.append(tuple(contour[e][0]))
            midPoint = averageDefects(defect[0], longestDefects[idx + 1][0], contour)
            fingerPoints.append(midPoint)
        elif idx == largestIdx:
            fingerPoints.append(tuple(contour[s][0]))
            #midPoint = averageDefects(longestDefects[idx - 1][0], defect[0], contour)
            #fingerPoints.append(midPoint)
        else:
            #average out two adjacent contours
            midPoint = averageDefects(defect[0], longestDefects[idx + 1][0], contour)
            fingerPoints.append(midPoint)

    return fingerPoints

def drawAngleAndBottomLine(img, dirUp, bottomline):
    start = (0, bottomline)
    end = (width, bottomline)
    cv2.line(img, start, end, (0,255,255), thickness=3)


def getFingerPointsFromHull(hull, isUp, centerOfHand):

    #one per finger
    k = 5
    filteredCenters = None
    centers = None
    kmeansHull = []
    for elem in hull:
        if isUp:
            if elem[0][1] <= centerOfHand[1]:
                kmeansHull.append([np.float32(elem[0][0]), np.float32(elem[0][1])])
        elif isUp is False:
            if elem[0][1] >= centerOfHand[0]:
                kmeansHull.append([np.float32(elem[0][0]), np.float32(elem[0][1])])
    kmeansHull = np.asarray(kmeansHull)
    if len(kmeansHull) >= k:
        #get the k means
        maxIters = 100
        criteria = (cv2.TERM_CRITERIA_EPS, 10, 0.1)
        retval, bestLabels, centers = cv2.kmeans(kmeansHull, k, criteria, maxIters, cv2.KMEANS_PP_CENTERS)

    return centers


def getLongestNDefectsinDirection(defects, n, clockwise=True):
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


def getFingerConvexDefects(img, defects, contour, center, dirUp):

    defects = getLongestNDefectsinDirection(defects, 4)
    filteredDefects = []
    for defect in defects:
        s, e, f, d = defect[0]
        start = tuple(contour[s][0])
        farthest = tuple(contour[f][0])
        end = tuple(contour[e][0])

        if dirUp:
            if start[1] < center[1] and farthest[1] < center[1] and end[1] < center[1]:
                filteredDefects.append(defect)
                cv2.line(img, start, farthest, (0,255,0), thickness=5)
                cv2.line(img, farthest, end, (0,255,0), thickness=5)
        elif dirUp is False:
            if start[1] < center[1] and farthest[1] < center[1] and end[1] < center[1]:
                filteredDefects.append(defect)
                cv2.line(img, start, farthest, (0,255,0), thickness=5)
                cv2.line(img, farthest, end, (0,255,0), thickness=5)

    return defects

def drawHull(img, hull):
    for idx in range(len(hull) - 1):
        cv2.line(img, tuple(hull[idx][0]), tuple(hull[idx + 1][0]), (0,255,255), thickness=10)
    cv2.line(img, tuple(hull[0][0]), tuple(hull[-1][0]), (0, 255, 255), thickness= 10)

def buildBottomFilter(diff, isUp, bottomline):
    if isUp:
        for idx in range(bottomline, len(diff)):
            row = diff[idx]
            for elemIdx in range(len(row)):
                row[elemIdx] = 0

    elif isUp is False:
        for idx in range(len(diff) - 1, bottomline, -1):
            row = diff[idx]
            for elemIdx in range(len(row)):
                row[elemIdx] = 0

    return diff


cap = cv2.VideoCapture(0)
code, background = cap.read()

fgbg = cv2.BackgroundSubtractorMOG2()


while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame, learningRate=0.1)
    cv2.imshow('Foreground', fgmask)
    cv2.imshow('Original', frame)
    if cv2.waitKey(10) == 27:
        break

threshVal = 75


blackImg = np.zeros((424,512,3), np.uint8)
blackImgCopy = blackImg.copy()
blurPixelSize = 17
dirUp = True
bottomline = 300
bottomFilter = blackImgCopy.copy()

contours = None

frameIdx = 0

while True:
    ret, img = cap.read()
    diff = fgbg.apply(img)

    diff = buildBottomFilter(diff, dirUp, bottomline)

    blackImgCopy = blackImg.copy()
    drawAngleAndBottomLine(blackImgCopy, dirUp, bottomline)

    blur = cv2.medianBlur(diff, blurPixelSize)

    ret, thresh1 = cv2.threshold(blur, threshVal, 255, cv2.THRESH_BINARY)



    contours, contourHeirarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    maxlen = 0
    largCont = []
    for cont in contours:
        if len(cont) > maxlen:
            maxlen = len(cont)
            largCont = cont


    if len(largCont) > 0:
        cv2.drawContours(blackImgCopy, largCont, -1, (255,255,255), thickness=5)
        cv2.fillPoly(blackImgCopy, pts=[largCont], color=(255,255,255))

        hullForDefects = cv2.convexHull(largCont, returnPoints=False)
        hull = cv2.convexHull(largCont)
        drawHull(blackImgCopy, hull)
        centerOfHand = cv2.moments(largCont, binaryImage=1)
        if centerOfHand['m00'] != 0:
            centerX = int(centerOfHand['m10']/centerOfHand['m00'])
            centerY = int(centerOfHand['m01']/centerOfHand['m00'])
            centerY += centerY*0.15
            cv2.circle(blackImgCopy, (centerX, int(centerY)), 5, (255, 255, 0), thickness=5)
            fingerPoints = getFingerPointsFromHull(hull, dirUp, (centerX, centerY))
            drawFingerCoords(blackImgCopy, fingerPoints)

            if len(hull) > 3:
                pdb.set_trace()
                defects = cv2.convexityDefects(largCont, hullForDefects)
                if defects is not None and len(defects) > 0:
                    defects = getFingerConvexDefects(blackImgCopy, defects, largCont, (centerX, centerY), dirUp)
                    #fingerCoords = getFingerPointsFromDefect(defects, largCont)
                    #for fingerCoord in fingerCoords:
                        #cv2.circle(blackImgCopy, fingerCoord, 5, (255, 0, 255), thickness=5)
                    #    pass
                    #cv2.imshow('image', blackImgCopy)
                else:
                    pass
        else:
            pass
    else:
        cv2.drawContours(blackImgCopy, largCont, -1, (255, 255, 255))


    cv2.imshow('transformed image', blur)

    k = cv2.waitKey(10)
    if k == 27:
        break
    elif k == ord('q') and blurPixelSize < 30:
        blurPixelSize += 2
    elif k == ord('w') and blurPixelSize > 2:
        blurPixelSize -= 2
    elif k == ord('a') and threshVal < 251:
        threshVal += 5
    elif k == ord('s') and threshVal > 6:
        threshVal -= 5
