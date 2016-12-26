import cv2
import Kinect.Kinect as Kinect
import FingerDetector as FD


class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        self.fd = FD.FingerDetector(300, 27, 159, False, self.kinect)


    def controlLoop(self):
        while True:
            frame = self.kinect.getFrame(self.kinect.rgbSharedMem)
            fingerPoints, fingerImage = self.fd.getFingerPositions()
            k = cv2.waitKey(10)

            if k == 27:
                break
            else:
                self.fd.adjustParams(k)

            cv2.imshow('fingers', fingerImage)


main = Main()
main.controlLoop()
