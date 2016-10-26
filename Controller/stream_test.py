import sys
sys.path.append("/home/evan/.virtualenvs/cv/local/lib/python2.7/site-packages")

import numpy as np
import cv2
import freenect

def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
    return array

fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    frame = get_video()

    fgmask = fgbg.apply(frame)

    cv2.imshow('Frame', fgmask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
