from shapedetector import ShapeDetector
import argparse
import imutils
import cv2

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
sd = ShapeDetector()

# while True:
#     k = cv2.waitKey(delay = 1)
#                 if k == ord('q'):
#                     self.kinect.device.stop()
#                     self.kinect.device.close()

for c in cnts:
    print len(c)
    print "----------"
    M = cv2.moments(c)

    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)

    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
