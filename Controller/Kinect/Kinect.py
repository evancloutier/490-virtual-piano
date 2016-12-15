import sys
from PIL import Image
sys.path.append('/usr/local/lib/python2.7/site-packages')
import sysv_ipc
import struct
import cv2
import numpy


sharedMemKeyLoc = "memkey.txt"
rgbIdx = 0
depthIdx = 1
width = 512
height = 424

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
        pilImage = Image.frombytes("RGB", (width, height), imgBuff)
        pilImage.save("/home/evan/rgb.png", "PNG")
        cv2Image = numpy.array(pilImage)
        return cv2Image

    def invertImage(self, cv2Im):
        revIm = (255 - cv2Im)
        cv2.imwrite("/home/evan/reverse.png", revIm)


kinect = Kinect()
cv2Im = kinect.getImage(kinect.rgbSharedMem)
#trivial image inversion
kinect.invertImage(cv2Im)
