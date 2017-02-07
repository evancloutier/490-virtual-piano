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

        self.keyBounds = None
        self.colorHandBounds = None
        self.depthHandBounds = None

    def getFrame(self):
        self.frames = self.listener.waitForNewFrame()

        arrayMap = dict()
        color = self.frames["color"].asarray()
        depth = self.frames["depth"].asarray()

        if self.keyBounds is not None and len(self.keyBounds) == 4:
            color = color[self.keyBounds[1]: self.keyBounds[3], self.keyBounds[0]: self.keyBounds[2]]

        arrayMap["color"] = color
        arrayMap["depth"] = depth

        return arrayMap

    def getHandColorFrame(self, frame):
        if self.colorHandBounds is not None:
            return frame[self.colorHandBounds[1]: self.colorHandBounds[3], self.colorHandBounds[0]: self.colorHandBounds[2]]
        else:
            return frame

    def getHandDepthFrame(self, colorFrame, depthFrame):
        if self.colorHandBounds is not None:
            # Retrieve the bounds on color frame
            x1, y1, x2, y2 = self.colorHandBounds
            print "({0}, {1}), ({2}, {3})".format(x1, y1, x2, y2)

            # Get row, col of color frame
            cCol, cRow, _ = colorFrame.shape
            dCol, dRow = depthFrame.shape

            print "cCol: {0}, cRow: {1}".format(cCol, cRow)
            print "dCol: {0}, dRow: {1}".format(dCol, dRow)

            dY1 = int((float(dCol) / float(cCol)) * float(y1))
            dX1 = int((float(dRow) / float(cRow)) * float(x1))
            dY2 = int((float(dCol) / float(cCol)) * float(y2))
            dX2 = int((float(dRow) / float(cRow)) * float(x2))

            print "({0}, {1}), ({2}, {3})".format(dX1, dY1, dX2, dY2)

            return depthFrame[dY1: dY2, dX1: dX2]
        else:
            return depthFrame



        # if self.colorHandBounds is not None:
        #     # Retrieve bounds on color frame
        #     (x1, y1, x2, y2) = self.colorHandBounds
        #
        #     # Convert bounds to depth frame
        #     dRow, dCol = depthFrame.shape
        #     cRow, cCol, _ = colorFrame.shape
        #
        #     dY1 = int((float(dCol) / float(cCol)) * float(y1))
        #     dX1 = int((float(dRow) / float(cRow)) * float(x1))
        #     dY2 = int((float(dCol) / float(cCol)) * float(y2))
        #     dX2 = int((float(dRow) / float(cRow)) * float(x2))
        #
        #     return depthFrame[dY1: dY2, dX1: dX2]
        # else:
        #     return depthFrame

    # def setDepthBounds(self):
    #     if self.depthBounds is None:
    #         x1, y1, x2, y2 = self.keyBounds
    #
    #         # Need to scale the points to fit within the depth frame
    #         dY1 = int((float(424) / float(1080)) * float(y1))
    #         dX1 = int((float(512) / float(1920)) * float(x1))
    #         dY2 = int((float(424) / float(1080)) * float(y2))
    #         dX2 = int((float(512) / float(1920)) * float(x2))
    #
    #         self.depthHandBounds = (dX1, dY1, dX2, dY2)



    def releaseFrame(self):
        self.listener.release(self.frames)

    def exit(self):
        self.device.stop()
        self.device.close()
        sys.exit(0)
