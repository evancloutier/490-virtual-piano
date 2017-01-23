import cv2
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector


class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        self.keyDetector = KeyDetector.KeyDetector(self.kinect)
        leftLineX, rightLineX, bottomLineY = self.keyDetector.getBounds()
        blurSize = 7
        threshVal = 159
        self.fingerDetector = FingerDetector.FingerDetector(leftLineX, rightLineX, bottomLineY, blurSize, threshVal, False, self.kinect)

    def controlLoop(self):
        #keyCoords = getKeyPositions
        while True:
            frame = self.kinect.getFrame(self.kinect.rgbSharedMem)
            fingerPoints, fingerImage = self.fingerDetector.getFingerPositions(frame)

            #for fingerPoint in fingerPoints:
                #key = getkeyFromFinger(fingerCoord)
                #isPressed = getDepthOfKey(key)
                #if isPressed:
                    #pressedKeys.append(key)

            k = cv2.waitKey(10)

            if k == 27:
                break
            else:
                self.fingerDetector.adjustParams(k)

            cv2.imshow('fingers', fingerImage)
            cv2.imshow('normal', frame)


main = Main()
main.controlLoop()
