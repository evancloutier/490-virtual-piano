import cv2
import Kinect.Kinect as Kinect
import FingerDetector as FD


class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        self.fd = FD.FingerDetector(500, 9, 159, False, self.kinect)


    def controlLoop(self):
        #keyCoords = getKeyPositions
        while True:
            frame = self.kinect.getFrame(self.kinect.rgbSharedMem)
            fingerPoints, fingerImage = self.fd.getFingerPositions(frame)

            #for fingerPoint in fingerPoints:
                #key = getkeyFromFinger(fingerCoord)
                #isPressed = getDepthOfKey(key)
                #if isPressed:
                    #pressedKeys.append(key)

            k = cv2.waitKey(10)

            if k == 27:
                break
            else:
                self.fd.adjustParams(k)

            cv2.imshow('fingers', fingerImage)
            #cv2.imshow('normal', frame)


main = Main()
main.controlLoop()
