import cv2
#import Kinect.Kinect as Kinect
import FingerDetector as FD


class Main:
    def __init__(self):
        #self.kinect = Kinect()
        self.fd = FD.FingerDetector(300, 27, 159, False)

    def controlLoop(self):
        #while True:
        #frame = self.fd.getFrame()

            #frame = kinect.get
        self.fd.continuousFingers()

#main = Main()
#main.controlLoop()
