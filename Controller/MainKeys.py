
# coding: utf-8

import numpy as np
import cv2
import sys
import KeyDetector as kd
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

# Create and set logger
logger = createConsoleLogger(LoggerLevel.Debug)
setGlobalLogger(logger)

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

listener = SyncMultiFrameListener(FrameType.Color)

# Register listener
device.setColorFrameListener(listener)
device.start()

color_depth_map = np.zeros((424, 512),  np.int32).ravel() \

keyDetector = kd.KeyDetector();

while True:
    frames = listener.waitForNewFrame()

    color = frames["color"]
    keyDetector.receiveFrame(color)
    
    #do processing of data in the key detector class here

    cv2.imshow("color", cv2.resize(keyDetector.transmitFrame(),
                                   (int(1920 / 3), int(1080 / 3))))

    listener.release(frames)

    key = cv2.waitKey(delay=1)
    if key == ord('q'):
        break

device.stop()
device.close()

sys.exit(0)