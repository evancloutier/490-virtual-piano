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

        self.keyThreshold = [1] * 8
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

            # Move this garbage into a function
            cv2.putText(depth, str(self.keyThreshold[0]), (30, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[1]), (96, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[2]), (160, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[3]), (226, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[4]), (292, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[5]), (358, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[6]), (424, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(depth, str(self.keyThreshold[7]), (490, 212), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.rectangle(depth, (0, 0), (64, 424), (0, 255, 0), 3)
            cv2.rectangle(depth, (64, 0), ((64 * 2), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 2), 0), ((64 * 3), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 3), 0), ((64 * 4), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 4), 0), ((64 * 5), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 5), 0), ((64 * 6), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 6), 0), ((64 * 7), 424), (0, 255, 0), 3)
            cv2.rectangle(depth, ((64 * 7), 0), ((64 * 8), 424), (0, 255, 0), 3)

            cv2.imshow("Depth", depth / 4500.)
            cv2.imshow("Filtered Image", filteredIm)


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
                if self.keyThreshold[0] > 0:
                    self.keyThreshold[0] -= 0.05
                    print "Key Threshold 0: {0}".format(self.keyThreshold[0])
            elif k == ord('w') or k == 1048695:
                if self.keyThreshold[0] < 10:
                    self.keyThreshold[0] += 0.05
                    print "Key Threshold 0: {0}".format(self.keyThreshold[0])
            elif k == ord('e') or k == 1048677:
                if self.keyThreshold[1] > 0:
                    self.keyThreshold[1] -= 0.05
                    print "Key Threshold 1: {0}".format(self.keyThreshold[1])
            elif k == ord('r') or k == 1048690:
                if self.keyThreshold[1] < 10:
                    self.keyThreshold[1] += 0.05
                    print "Key Threshold 1: {0}".format(self.keyThreshold[1])
            elif k == ord('a') or k == 1048673:
                if self.keyThreshold[2] > 0:
                    self.keyThreshold[2] -= 0.05
                    print "Key Threshold 2: {0}".format(self.keyThreshold[2])
            elif k == ord('s') or k == 1048691:
                if self.keyThreshold[2] < 10:
                    self.keyThreshold[2] += 0.05
                    print "Key Threshold 2: {0}".format(self.keyThreshold[2])
            elif k == ord('d') or k == 1048676:
                if self.keyThreshold[3] > 0:
                    self.keyThreshold[3] -= 0.05
                    print "Key Threshold 3: {0}".format(self.keyThreshold[3])
            elif k == ord('f') or k == 1048678:
                if self.keyThreshold[3] < 10:
                    self.keyThreshold[3] += 0.05
                    print "Key Threshold 3: {0}".format(self.keyThreshold[3])
            elif k == ord('y'):
                if self.keyThreshold[4] > 0:
                    self.keyThreshold[4] -= 0.05
                    print "Key Threshold 4: {0}".format(self.keyThreshold[4])
            elif k == ord('u'):
                if self.keyThreshold[4] < 10:
                    self.keyThreshold[4] += 0.05
                    print "Key Threshold 4: {0}".format(self.keyThreshold[4])
            elif k == ord('i'):
                if self.keyThreshold[5] > 0:
                    self.keyThreshold[5] -= 0.05
                    print "Key Threshold 5: {0}".format(self.keyThreshold[5])
            elif k == ord('o'):
                if self.keyThreshold[5] < 10:
                    self.keyThreshold[5] += 0.05
                    print "Key Threshold 5: {0}".format(self.keyThreshold[5])
            elif k == ord('h'):
                if self.keyThreshold[6] > 0:
                    self.keyThreshold[6] -= 0.05
                    print "Key Threshold 5: {0}".format(self.keyThreshold[6])
            elif k == ord('j'):
                if self.keyThreshold[6] < 10:
                    self.keyThreshold[6] += 0.05
                    print "Key Threshold 6: {0}".format(self.keyThreshold[6])
            elif k == ord('k'):
                if self.keyThreshold[7] > 0:
                    self.keyThreshold[7] -= 0.05
                    print "Key Threshold 7: {0}".format(self.keyThreshold[7])
            elif k == ord('l'):
                if self.keyThreshold[7] < 10:
                    self.keyThreshold[7] += 0.05
                    print "Key Threshold 6: {0}".format(self.keyThreshold[7])

main = Main()
main.initializeDepthLoop()
main.controlLoop()
