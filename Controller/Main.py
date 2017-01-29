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
        # self.keyDetector = KeyDetector.KeyDetector(self.kinect)
        self.boundsDetector = BoundsDetector.BoundsDetector(self.kinect)

    def controlLoop(self):
        while True:
            frame = self.kinect.getFrame(ft.Color)
            bounds = self.boundsDetector.getROIBounds()

            # numpy slicing to get our ROI
            boundedImage = frame[bounds[1]: bounds[3], bounds[0]: bounds[2]]

            # for contour in self.keyDetector.contours:
            #     c = contour[0]
            #     cv2.drawContours(frame, [c], -1, (0, 0, 0), 5)
            #     cv2.circle(frame, (contour[1], contour[2]), 7, (0, 0, 0), -1)

            cv2.imshow("Stream", boundedImage)
            # cv2.imshow("Stream", cv2.resize(boundedImage, (int(1920 / 3), int(1080 / 3))))
            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break


        # keyCoords = getKeyPositions
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
