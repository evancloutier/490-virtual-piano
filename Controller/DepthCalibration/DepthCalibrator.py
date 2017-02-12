# coding: utf-8

import numpy as np
import cv2
import sys
import math
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel



class DepthCalibrator:
    
    def processDepthFrame(self, depth):
        row, col = depth.shape

        # Create array to normalize depth values
        norm = np.zeros((row, col))
        norm.fill(1000)
        normDepth = depth / norm

        # Apply grayscale value to array
        for index, x in np.ndenumerate(normDepth):
            if math.isnan(x):
                continue
            else:
                updated = self.getGrayscaleValue(1, 0, x)
                normDepth.itemset(index, updated)

        # Cast to np.uint8
        grayDepth = normDepth.astype(np.uint8, copy = True)

        # Convert grayscale value to RGB
        colorDepth = cv2.cvtColor(grayDepth, cv2.COLOR_GRAY2RGB)

        # Apply color map to RGB array
        colorMap = cv2.applyColorMap(colorDepth, cv2.COLORMAP_JET)
        

        # Return it to display
        return colorMap

    def getGrayscaleValue(self, highBound, lowBound, value):
        if math.isnan(value):
            return 0
        else:
            return int(((255) * (value - lowBound)) / (highBound - lowBound) + lowBound)
    
    def getMouseCoordsColor(something, event,  x, y, flags, param ):
        global xColor, yColor
        if event == cv2.EVENT_LBUTTONDOWN:
            xColor, yColor = x, y
            print "xColor: ", xColor
            print "yColor: ", yColor
            
    def getMouseCoordsDepth(something, event,  x, y, flags, param ):
        global xDepth, yDepth
        if event == cv2.EVENT_LBUTTONDOWN:
            xDepth, yDepth = x, y
            
    
    def controlLoop(self):
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

        listener = SyncMultiFrameListener(FrameType.Color | FrameType.Depth)

        # Register listeners
        device.setColorFrameListener(listener)
        device.setIrAndDepthFrameListener(listener)

        device.start()

        otsuThresh = 127
        
        while True:
            frames = listener.waitForNewFrame()

            color = frames["color"].asarray()
            depth = frames["depth"].asarray()
            
            cv2.imshow("color", color)
            cv2.setMouseCallback("color", self.getMouseCoordsColor)
            
            cv2.imshow("depth", self.processDepthFrame(depth))
            cv2.setMouseCallback("depth", self.getMouseCoordsDepth)
            
            
            listener.release(frames)

            key = cv2.waitKey(delay=1)
            if key == ord('q'):
                break
            if key == ord('d'):
                print "depthX: ", xDepth
                print "depthY: ", yDepth
            if key == ord('c'):
                print "colorX: ", xColor
                print "colorY: ", yColor
                
            

        device.stop()
        device.close()

        sys.exit(0)

        
dc = DepthCalibrator()
dc.controlLoop()