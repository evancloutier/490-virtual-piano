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

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break

        tens = np.zeros((424, 512))
        tens.fill(10)
        self.depthProcessor.depthValues = self.depthProcessor.sumDepthValues / tens
        print np.amax(self.depthProcessor.sumDepthValues)
        print np.amax(self.depthProcessor.depthValues)
        end = time.time()
        print "Done initializing, took ", end - start, "seconds"

    def controlLoop(self):

        while True:
            frame = self.kinect.getFrame()
            frames = self.kinect.frames
            color = frame["color"]
            depth = frame["depth"]


            filteredIm, backProject = self.fingerDetector.applyHistogram(color)
            self.kinect.colorHandBounds = self.boundsDetector.getBoundingBoxOfHand(self.fingerDetector.hand)

            x1, y1, x2, y2 = self.kinect.colorHandBounds

            cv2.rectangle(color, (x1, y1), (x2, y2), (0, 0, 0), 2)


            filteredHandIm = self.kinect.getHandColorFrame(filteredIm)
            #if len(filteredHandIm) > 0 and len(filteredHandIm[0]) > 0:
            #    cv2.imshow("filtered hand im", filteredHandIm)

            fingerIm, fingerPoints = self.fingerDetector.getFingerPositions(filteredHandIm, x1, y1)

            keysBeingHovered = self.fingerMapper.getKeysBeingHovered(fingerPoints, self.keyDetector.keys)

            #print "keys being hovered:", keysBeingHovered

            #check to see if the finger points are being pressed
            keysBeingPressed = self.depthProcessor.checkFingerPoints(depth, keysBeingHovered)

            #print "keys being pressed without matrix:", keysBeingPressed


            keysBeingPressed = self.depthProcessor.calculateNotesMatrix(keysBeingPressed)

            print "keys being pressed with matrix:", keysBeingPressed

            self.writeNotes.writeKeyNamesToFile(keysBeingPressed)


            if fingerIm is not None:
                if len(fingerIm) > 0 and len(fingerIm[0]) > 0:
                    cv2.imshow("finger im", fingerIm)

            if fingerPoints is not None:
                for point in fingerPoints:
                    cv2.circle(color, (point[0], point[1]), 4, color=(255,255,0), thickness=3)


            #cv2.imshow("color", color)
            #cv2.imshow("depth", depth / 4500.)
            #cv2.imshow("Average depth value", self.depthProcessor.depthValues)

            #handDepthFrame = self.kinect.getHandDepthFrame(color, depth)
            #handDepthColorMap = self.depthProcessor.processDepthFrame(handDepthFrame)


            self.kinect.releaseFrame()

            k = cv2.waitKey(10)

            if k == 27:
                cv2.destroyAllWindows()
                self.kinect.exit()
                break
            #else:
            #    self.fingerDetector.adjustParams(k)



main = Main()
main.initializeDepthLoop()
main.controlLoop()
