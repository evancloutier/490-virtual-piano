import cv2
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector
import BoundsDetector
import FrameType

ft = FrameType.FrameType()

class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        # self.boundsDetector = BoundsDetector.BoundsDetector(self.kinect)
        # leftLineX, rightLineX, bottomLineY = self.keyDetector.getBounds()
        # blurSize = 7
        # threshVal = 159
        # self.fingerDetector = FingerDetector.FingerDetector(leftLineX, rightLineX, bottomLineY, blurSize, threshVal, False, self.kinect)

    def controlLoop(self):
        while True:
            frame = self.kinect.getFrame(ft.Color)

            # for contour in self.keyDetector.contours:
            #     c = contour[0]
            #     cv2.drawContours(frame, [c], -1, (0, 0, 0), 5)
            #     cv2.circle(frame, (contour[1], contour[2]), 7, (0, 0, 0), -1)

            cv2.imshow("Depth", cv2.resize(frame, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break


        #keyCoords = getKeyPositions
        # while True:
        #     frame = self.kinect.getFrame(ft.Color)
        #     # fingerPoints, fingerImage = self.fingerDetector.getFingerPositions(frame)
        #
        #     #for fingerPoint in fingerPoints:
        #         #key = getkeyFromFinger(fingerCoord)
        #         #isPressed = getDepthOfKey(key)
        #         #if isPressed:
        #             #pressedKeys.append(key)
        #
        #     k = cv2.waitKey(10)
        #
        #     if k == 27:
        #         break
        #     else:
        #         self.fingerDetector.adjustParams(k)
        #
        #     cv2.imshow('fingers', fingerImage)
        #     cv2.imshow('normal', frame)


main = Main()
main.controlLoop()
