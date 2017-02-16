import cv2
import numpy as np
import time
import Kinect.Kinect as Kinect
import FingerDetector
import KeyDetector
import BoundsDetector
import DepthProcessor
import FingerMapper
import WriteNotes

class Main:
    def __init__(self):
        self.kinect = Kinect.Kinect()
        blurSize = 7
        threshVal = 159

        self.keyThreshold = 10
        self.writeNotes = WriteNotes.WriteNotes()
        self.fingerMapper = FingerMapper.FingerMapper()
        self.fingerDetector = FingerDetector.FingerDetector(blurSize, threshVal, False, self.kinect)
        self.fingerDetector.buildSkinColorHistogram(self.kinect)
        self.boundsDetector = BoundsDetector.BoundsDetector(self.kinect)
        self.kinect.keyBounds = self.boundsDetector.getROIBounds()
        self.keyDetector = KeyDetector.KeyDetector(self.kinect, "C")
        self.depthProcessor = DepthProcessor.DepthProcessor(self.kinect)

    def initializeDepthLoop(self):
        counter = 0

        print("Initializing depth matrix...")
        start = time.time()
        while counter < 10:
            frame = self.kinect.getFrame()
            depth = frame["depth"]
            self.depthProcessor.initializeDepthMap(depth, counter)

            self.kinect.releaseFrame()
            counter += 1

            k = cv2.waitKey(10)

            if k == 27 or k == 1048603:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break

        tens = np.zeros((424, 512))
        tens.fill(10)
        self.depthProcessor.depthValues = self.depthProcessor.sumDepthValues / tens
        print np.amax(self.depthProcessor.sumDepthValues)
        print np.amax(self.depthProcessor.depthValues)
        frame = self.kinect.getFrame()
        frames = self.kinect.frames
        self.depthProcessor.buildNormalizedThresholdMatrix(frames["depth"])
        self.kinect.releaseFrame()

        end = time.time()
        print "Done initializing, took ", end - start, "seconds"

    def controlLoop(self):

        while True:
            frame = self.kinect.getFrame()
            frames = self.kinect.frames
            color = frame["color"]
            depth = frame["depth"]


            filteredIm, backProject = self.fingerDetector.applyHistogram(color)
            totalKeysBeingPressed = []

            hand = self.fingerDetector.hand1
            for i in range(2):
                self.kinect.colorHandBounds = self.boundsDetector.getBoundingBoxOfHand(hand)
                x1, y1, x2, y2 = self.kinect.colorHandBounds

                filteredHandIm = self.kinect.getHandColorFrame(filteredIm)
                fingerIm, fingerPoints = self.fingerDetector.getFingerPositions(filteredHandIm, x1, y1, hand)

                keysBeingHovered = self.fingerMapper.getKeysBeingHovered(fingerPoints, self.keyDetector.keys)

                keysBeingPressed = self.depthProcessor.checkFingerPoints(depth, keysBeingHovered, self.keyThreshold)
                keysBeingPressed = self.depthProcessor.calculateNotesMatrix(keysBeingPressed, i)


                totalKeysBeingPressed.extend(keysBeingPressed)

                if len(filteredHandIm) > 0 and len(filteredHandIm[0]) > 0:
                    if i == 0:
                        h1 = np.copy(filteredHandIm)
                        f1 = np.copy(fingerIm)
                        #cv2.imshow("Filtered Hand Image", h1)
                        if f1 is not None:
                            if len(f1) > 0 and len(f1[0]) > 0:
                                p = 1
                                cv2.imshow("finger im", f1)
                    elif i == 1:
                        h2 = np.copy(filteredHandIm)
                        f2 = np.copy(fingerIm)
                        #cv2.imshow("Other hand im", h2)
                        if f2 is not None:
                            if len(f2) > 0 and len(f2[0]) > 0:
                                p = 1
                                cv2.imshow("second finger im", f2)
                hand = self.fingerDetector.hand2

            cv2.imshow("filtered Image", filteredIm)
            print "Keys being pressed without matrix: {0}".format(totalKeysBeingPressed)
            print "Keys being pressed with matrix: {0}".format(totalKeysBeingPressed)

            self.writeNotes.writeKeyNamesToFile(totalKeysBeingPressed)


            # if fingerIm is not None:
            #     if len(fingerIm) > 0 and len(fingerIm[0]) > 0:
            #         cv2.imshow("finger im", fingerIm)

            # if fingerPoints is not None:
            #     for point in fingerPoints:
            #         cv2.circle(color, (point[0], point[1]), 4, color=(255,255,0), thickness=3)


            #cv2.imshow("color", color)
            #cv2.imshow("normalized", self.depthProcessor.normalizedThresholdMatrix)
            #cv2.imshow("depth", depth / 4500.)
            ##cv2.imshow("Average depth value", self.depthProcessor.depthValues)

            ##handDepthFrame = self.kinect.getHandDepthFrame(color, depth)
            ##handDepthColorMap = self.depthProcessor.processDepthFrame(handDepthFrame)


            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27 or k == 1048603:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break
            elif k == ord('q') or k == 1048689:
                if self.keyThreshold > 5:
                    self.keyThreshold -= 0.2
                    print "Key Threshold: {0}".format(self.keyThreshold)
            elif k == ord('w') or k == 1048695:
                if self.keyThreshold < 20:
                    self.keyThreshold += 0.2
                    print "Key Threshold: {0}".format(self.keyThreshold)

            #else:
            #    self.fingerDetector.adjustParams(k)



main = Main()
main.initializeDepthLoop()
main.controlLoop()
