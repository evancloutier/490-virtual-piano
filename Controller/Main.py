import cv2
import numpy as np
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector
import BoundsDetector

class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        blurSize = 7
        threshVal = 159

        self.fingerDetector = FingerDetector.FingerDetector(blurSize, threshVal, False, self.kinect)
        self.fingerDetector.buildSkinColorHistogram(self.kinect)
        self.boundsDetector = BoundsDetector.BoundsDetector(self.kinect)
        self.kinect.bounds = self.boundsDetector.getROIBounds()
        self.keyDetector = KeyDetector.KeyDetector(self.kinect, "C")


    def controlLoop(self):

        while True:
            frame = self.kinect.getFrame()
            color = frame["color"]
            depth = frame["depth"]

            filteredIm, backProject = self.fingerDetector.applyHistogram(color)
            fingerIm, fingerPoints = self.fingerDetector.getFingerPositions(filteredIm)

            self.keyDetector.drawKeys(color)
            #for idx in fingerPoints:
            #    cv2.circle(color, (fingerPoints[idx][0], fingerPoints[idx][1]), 4, color=(0,255,0), thickness=3)


            # bounds = self.boundsDetector.getROIBounds()
            # boundedColor = colorArray[bounds[1]: bounds[3], bounds[0]: bounds[2]]
            # boundedDepth = depthArray[bounds[1]: bounds[3], bounds[0]: bounds[2]]
            #
            #for contour in self.keyDetector.contours:
            #    c = contour[0]
            #    cv2.drawContours(color, [c], -1, (0, 0, 0), 2)
            #    cv2.circle(color, (contour[1], contour[2]), 4, (0, 0, 0), -1)
            #
            # cv2.imshow("Bounded Color", cv2.resize(boundedColor, (int(1920 / 3), int(1080 / 3))))
            # cv2.imshow("Bounded Depth", boundedDepth / 4500.)
            #

            # self.kinect.registration.apply(color, depth, self.kinect.undistorted, self.kinect.registered, None, None)
            #
            # cv2.circle(self.kinect.registered.asarray(np.uint8), (300, 300), 7, (255, 0, 0), -1)
            # cv2.circle(depth.asarray(), (300, 300), 7, (255, 0, 0), -1)
            # (x, y, z) = self.kinect.registration.getPointXYZ(self.kinect.undistorted, 300, 300)
            # print "X: {0}, Y: {1}, Z: {2}".format(x, y, z)
            #
            # cv2.imshow("Depth", depth.asarray() / 4500.)
            # cv2.imshow("Registered", self.kinect.registered.asarray(np.uint8))
            #

            #bounds = self.boundsDetector.getROIBounds()

            # numpy slicing to get our ROI
            #boundedImage = frame[bounds[1]: bounds[3], bounds[0]: bounds[2]]

            # cv2.imshow("Stream", boundedImage)
            #cv2.imshow("Stream", cv2.resize(boundedImage, (int(1920 / 3), int(1080 / 3))))
            cv2.imshow('raw im', color)#cv2.resize(color, (int(1920 / 3), int(1080 / 3))))

            cv2.imshow('filter', filteredIm)#cv2.resize(filteredIm, (int(1920 / 3), int(1080 / 3))))
            cv2.imshow('hand', fingerIm)#cv2.resize(fingerIm, (int(1920 / 3), int(1080 / 3))))

            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break
            #else:
            #    self.fingerDetector.adjustParams(k)

main = Main()
main.controlLoop()
