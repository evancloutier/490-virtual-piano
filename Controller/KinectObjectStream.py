#import the necessary modules
import sys
sys.path.append("/home/evan/.virtualenvs/cv/local/lib/python2.7/site-packages")

import freenect
import cv2 as cv
import numpy as np

class KinectObjectStream():

    def __init__(self):
        self.frame = None

    def get_frame(self):
        frame = self.get_video()
        return frame

    def display_image(self, image_data):
        cv.imshow('Image', image_data)

    def dispaly_rgb(self):
        while True:
            self.update_video()
            cv.imshow('RGB image',self.frame)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()

    #function to get RGB image from kinect
    def update_video(self):
        video_data,_ = freenect.sync_get_video()
        video_data = cv.cvtColor(video_data,cv.COLOR_RGB2BGR)
        self.frame = video_data

kos = KinectObjectStream()
kos.dispaly_rgb()
