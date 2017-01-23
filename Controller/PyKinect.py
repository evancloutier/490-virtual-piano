import sys
import cv2
import numpy as np

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

def initializeKinect():
    # Create and set logger
    logger = createConsoleLogger(LoggerLevel.Debug)
    setGlobalLogger(logger)

    # Initialize the Freenect2 instance
    fn = Freenect2()

    # Check for registered devices
    num_devices = fn.enumerateDevices()
    if num_devices == 0:
        print("No device connected!")
        return False

    # Register serial numbers and open device pipeline
    serial = fn.getDeviceSerialNumber(0)
    device = fn.openDevice(serial, pipeline = pipeline)

    # Initialize listener
    listener = SyncMultiFrameListener(FrameType.Color)

    # Register listener
    device.setColorFrameListener(listener)
    device.start()

    return [listener, device]
