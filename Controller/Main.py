import cv2
import numpy as np
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector
import BoundsDetector
import DepthProcessor

class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        blurSize = 7
        threshVal = 159

        self.boundsDetector = BoundsDetector.BoundsDetector(self.kinect)
        self.fingerDetector = FingerDetector.FingerDetector(blurSize, threshVal, False, self.kinect)
        self.fingerDetector.buildSkinColorHistogram(self.kinect)
        self.kinect.bounds = self.boundsDetector.getROIBounds()
        self.keyDetector = KeyDetector.KeyDetector(self.kinect)
        self.depthProcessor = DepthProcessor.DepthProcessor(self.kinect)

    def controlLoop(self):

        while True:
            frame = self.kinect.getFrame()

            color = frame["color"]
            depth = frame["depth"]

            # depthColor = self.depthProcessor.processDepthFrame(depth)

            cv2.imshow("Color", cv2.resize(color, (int(1920 / 3), int(1080 / 3))))
            # cv2.imshow("Depth Color Map", depthColor)

            filteredIm = self.fingerDetector.applyHistogram(color)
            fingerIm, fingerPoints = self.fingerDetector.getFingerPositions(filteredIm)

            # self.kinect.registration.apply(color, depth, self.kinect.undistorted, self.kinect.registered, None, None)
            #
            # cv2.circle(self.kinect.registered.asarray(np.uint8), (300, 300), 7, (255, 0, 0), -1)
            # cv2.circle(depth.asarray(), (300, 300), 7, (255, 0, 0), -1)
            # (x, y, z) = self.kinect.registration.getPointXYZ(self.kinect.undistorted, 300, 300)
            # print "X: {0}, Y: {1}, Z: {2}".format(x, y, z)

            # cv2.imshow("Registered", self.kinect.registered.asarray(np.uint8))

            cv2.imshow('filter', cv2.resize(filteredIm, (int(1920 / 3), int(1080 / 3))))
            cv2.imshow('hand', cv2.resize(fingerIm, (int(1920 / 3), int(1080 / 3))))

            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break
            else:
                self.fingerDetector.adjustParams(k)

main = Main()
main.controlLoop()
