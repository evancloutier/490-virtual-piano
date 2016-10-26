#import the necessary modules
import sys
sys.path.append("/home/evan/.virtualenvs/cv/local/lib/python2.7/site-packages")

import freenect
import cv2 as cv
import numpy as np

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv.cvtColor(array,cv.COLOR_RGB2BGR)
    return array

#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array

if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        print "Depth: {0}".format(depth)
        print "---------------------------------------"

        #display RGB image
        cv.imshow('RGB image',frame)
        #display depth image
        cv.imshow('Depth image',depth)

        # quit program when 'esc' key is pressed
        k = cv.waitKey(5) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows()
