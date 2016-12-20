import cv2
import time
import numpy as np

width = 512
height = 424


def averageDefects(defect1, defect2, contour):

    s1, e1, f1, d1 = defect1
    s2, e2, f2, d2 = defect2

    start = contour[s1][0]
    end = contour[e2][0]

    newX = (start[0] + end[0])/2
    newY = (start[1] + end[1])/2

    return (newX, newY)


def getFingerPoints(longestDefects, contour):
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


def getFingerConvexDefects(img, defects, contour):

    defects = getLongestNDefectsinDirection(defects, 4)

    for defect in defects:
        s, e, f, d = defect[0]
        start = tuple(contour[s][0])
        farthest = tuple(contour[f][0])
        end = tuple(contour[e][0])
        cv2.line(img, start, farthest, (0,255,0), thickness=5)
        cv2.line(img, farthest, end, (0,255,0), thickness=5)

    return defects

cap = cv2.VideoCapture(0)
code, background = cap.read()

while(cap.isOpened()):
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    cv2.imshow('blank background', hsv)
    background = hsv
    k = cv2.waitKey(10)
    if k == 27:
        break

threshVal = 75


blackImg = np.zeros((424,512,3), np.uint8)
blackImgCopy = blackImg.copy()
blurPixelSize = 17

contours = None

while True:
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    diff = cv2.absdiff(img, background)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    ret, thresh1 = cv2.threshold(diff, threshVal, 255, cv2.THRESH_BINARY)



    blur = cv2.medianBlur(thresh1, blurPixelSize)
    contours, contourHeirarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)



    maxlen = 0
    largCont = []
    for cont in contours:
        if len(cont) > maxlen:
            maxlen = len(cont)
            largCont = cont

    blackImgCopy = blackImg.copy()
    if len(largCont) != 0:
        cv2.fillPoly(blackImgCopy, pts=[largCont], color=(255,255,255))


    hullForDefects = cv2.convexHull(largCont, returnPoints=False)
    hull = cv2.convexHull(largCont)
    defects = cv2.convexityDefects(largCont, hullForDefects)
    defects = getFingerConvexDefects(blackImgCopy, defects, largCont)
    fingerCoords = getFingerPoints(defects, largCont)
    for fingerCoord in fingerCoords:
        cv2.circle(blackImgCopy, fingerCoord, 5, (255, 0, 255), thickness=5)



    cv2.imshow('soruce image', blackImgCopy)
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




