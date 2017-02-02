import numpy as np
import cv2
import sys
import platform
import pdb

system = platform.system()

'''if system != "Darwin":
    from PIL import Image
    sys.path.append('/usr/local/lib/python2.7/site-packages')
    import sysv_ipc
    import struct
'''
#else:
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

try:
    from pylibfreenect2 import OpenCLPacketPipeline
    pipeline = OpenCLPacketPipeline()
except:
    from pylibfreenect2 import CpuPacketPipeline
    pipeline = CpuPacketPipeline()

# Memory locations
sharedMemKeyLoc = "Kinect/memkey.txt"
# sharedMemKeyLoc = "memkey.txt"
semaphoreKeyLoc = "Kinect/semkey.txt"
# semaphoreKeyLoc = "semkey.txt"

# Index and bound values
rgbIdx = 0
depthIdx = 1
width = 1000
height = 500

# Semaphore booleans
semReading = 1
semWriting = 0

# This class will need to be updated later to retrieve depth

class Kinect:
    def __init__(self):
        #if system == 'Darwin':
        # Initialize the Freenect2 instance
        self.fn = Freenect2()

        # Check for registered devices
        num_devices = self.fn.enumerateDevices()
        if num_devices == 0:
            print "No device connected!"
            sys.exit(1)

        # Register serial numbers and open device pipeline
        self.serial = self.fn.getDeviceSerialNumber(0)
        self.pipeline = pipeline
        self.device = self.fn.openDevice(self.serial, pipeline = self.pipeline)

        # Initialize listener
        self.listener = SyncMultiFrameListener(FrameType.Color | FrameType.Depth)

        # Register listener
        self.device.setColorFrameListener(self.listener)
        self.device.setIrAndDepthFrameListener(self.listener)
        self.device.start()

        self.registration = Registration(self.device.getIrCameraParams(),
                                         self.device.getColorCameraParams())

        self.undistorted = Frame(512, 424, 4)
        self.registered = Frame(512, 424, 4)

        # Retrieve and release the first frame for initialization
        self.frames = self.listener.waitForNewFrame()
        self.listener.release(self.frames)

        self.bounds = None
        '''else:
            self.semaphoreKey = self.getSemaphoreKey()
            self.semaphore = self.getSharedMemByKey(self.semaphoreKey)
            self.rgbKey, self.depthKey = self.getSharedMemKeys()
            self.rgbSharedMem = self.getSharedMemByKey(self.rgbKey)
        '''

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

    def getSemaphoreKey(self):
        semFile = open(semaphoreKeyLoc)
        semKey = int(semFile.readlines()[0])
        return semKey

    def getSharedMemByKey(self, key):
        mem = sysv_ipc.SharedMemory(key)
        return mem

    def readMem(self, sharedMem):
        memVal = sharedMem.read()
        return memVal

    def getSemaphore(self):
        while True:
            semVal = bytearray(self.readMem(self.semaphore))[0]
            if semVal == semReading:
                return

    def releaseSemaphore(self):
        self.semaphore.write(chr(semWriting))

    def getFrame(self):
        #if system == 'Darwin':
        self.frames = self.listener.waitForNewFrame()

        #self.frames["depth"] = self.frames["depth"].asarray()
        arrayMap = dict()
        color = self.frames["color"].asarray()
        depth = self.frames["depth"].asarray()

        if self.bounds is not None and len(self.bounds) == 4:
            print self.bounds
            color = color[self.bounds[1]: self.bounds[3], self.bounds[0]: self.bounds[2]]

        arrayMap["color"] = color
        arrayMap["depth"] = depth

        return arrayMap
        '''else:
            self.getSemaphore()
            imgBuff = self.readMem(self.rgbSharedMem)
            self.releaseSemaphore()

            # We will need to account for the depth at a later point
            pilImage = Image.frombytes("RGB", (width, height), imgBuff)
            #pilImage.save("/home/evan/rgb.png", "PNG")
            cv2Image = np.array(pilImage)
            return cv2Image
        '''

    def releaseFrame(self):
        self.listener.release(self.frames)

    def exit(self):
        self.device.stop()
        self.device.close()
        sys.exit(0)
