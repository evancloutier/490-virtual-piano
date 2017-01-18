import argparse
import operator
import imutils
import cv2

# # TO-DO: Notes
# - We know how many sides each piano key is supposed to have, so correction can be applied if necessary
# - Need to create Key class to assign note and frequency values to each key
# ---> Enumerate number of sides and other direct information based on the key identified
# ---> We will also know where an octave starts and ends based on the number of contours identified (hopefully)
# - Need to extract the key points from each contour to relate their bounds to the hands

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image, width = 300)
ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

contours = []

for idx, c in enumerate(cnts):
    M = cv2.moments(c)

    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)

    contour = [idx, c, cX, cY]
    contours.append(contour)

contours.sort(key=lambda x: x[2])

octave = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
index = 0

for contour in contours:
    c = contour[1]
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")

    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (contour[2], contour[3]), 7, (0, 0, 0), -1)
    cv2.putText(image, octave[index], (contour[2], contour[3] - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    index += 1

    cv2.imshow("Image", image)
    cv2.waitKey(0)
