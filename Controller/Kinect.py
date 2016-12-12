import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import sysv_ipc
import struct
import cv2
import numpy


sharedMemKeyLoc = "Kinect/memkey.txt"
rgbIdx = 0
depthIdx = 1

class Kinect:
    def __init__(self):
        self.rgbKey, self.depthKey = self.getSharedMemKeys()
        self.rgbSharedMem = self.getSharedMemByKey(self.rgbKey)

    def getSharedMemKeys(self):
        keyFiles = open(sharedMemKeyLoc)
        rgbKey = 0
        depthKey = 0
        for idx, line in enumerate(keyFiles.readlines()):
            if idx == 0:
                rgbKey = int(line)
            elif idx == 1:
                depthKey = int(line)
        return [rgbKey, depthKey]

    def getSharedMemByKey(self, key):
        mem = sysv_ipc.SharedMemory(key)
        return mem

    def readMem(self, sharedMem):
        memVal = sharedMem.read()
        return memVal

    def getImage(self, sharedMem):
        imgBuff = self.readMem(sharedMem)
        imgArray = numpy.asarray(bytearray(imgBuff), dtype=numpy.uint8)
        print imgArray.size
        opencvImage = cv2.imdecode(imgArray, cv2.CV_LOAD_IMAGE_UNCHANGED)
        print "got here!"
        cv2.imwrite('animage.png', opencvImage)


kinect = Kinect()
kinect.getImage(kinect.rgbSharedMem)
