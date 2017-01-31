import cv2
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector


class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        self.keyDetector = KeyDetector.KeyDetector(self.kinect)
        blurSize = 7
        threshVal = 159
        self.fingerDetector = FingerDetector.FingerDetector(blurSize, threshVal, False, self.kinect)

    def controlLoop(self):
        self.fingerDetector.buildSkinColorHistogram(self.kinect)

        while True:
            frame = self.kinect.getFrame(self.kinect.rgbSharedMem)
            filteredIm = self.fingerDetector.applyHistogram(frame)
            fingerIm, fingerPoints = self.fingerDetector.getFingerPositions(filteredIm)

            k = cv2.waitKey(10)
            if k == 27:
                break
            else:
                self.fingerDetector.adjustParams(k)

            cv2.imshow('filter', filteredIm)
            cv2.imshow('hand', fingerIm)


main = Main()
main.controlLoop()
