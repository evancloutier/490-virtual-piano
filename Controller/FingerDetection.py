import cv2
import time
import numpy as np

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
'''
while(cap.isOpened()):
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    diff = cv2.absdiff(img, background)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

    ret, thresh1 = cv2.threshold(diff, threshVal, 255, cv2.THRESH_BINARY)
    #thresh1 = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, standardDev)

    cv2.imshow('thresholding', thresh1)
    hand = img
    k = cv2.waitKey(10)
    if k == 27:
        cv2.imwrite('threshold-hand.png', thresh1)
        break

'''

blackImg = np.zeros((424,512,3), np.uint8)

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

    #cv2.drawContours(blackImg, [largCont], 0, (255,255,255))

    blackImgCopy = blackImg.copy()
    if len(largCont) != 0:
        cv2.fillPoly(blackImgCopy, pts=[largCont], color=(255,255,255))

    cv2.imshow('soruce image', blackImgCopy)
    k = cv2.waitKey(10)
    if k == 27:
        break
    elif k == ord('q') and blurPixelSize < 30:
        blurPixelSize += 2
        print blurPixelSize
    elif k == ord('w') and blurPixelSize > 2:
        blurPixelSize -= 2
        print blurPixelSize
    elif k == ord('a') and threshVal < 251:
        threshVal += 5
    elif k == ord('s') and threshVal > 6:
        threshVal -= 5




otsuThresh = 100




