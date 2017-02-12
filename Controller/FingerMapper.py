import cv2
import numpy as np

class FingerMapper:
    def __init__(self):
        pass

    def getKeysBeingHovered(self, fingerPoints, keys):
        keysBeingHovered = dict()
        if fingerPoints is None or keys is None:
            return keysBeingHovered
        #we want to reference the fingerPoints with the area of the keyContours
        for key in keys:
            cnt = keys[key]
            for point in fingerPoints:
                #check if point in key contour
                if cv2.pointPolygonTest(cnt, (point[0], point[1]), False) == 1:
                    #get the corresponding key note from the contour
                    for key in keys:
                        if np.array_equal(keys[key], cnt):
                            keysBeingHovered[key] = point

        return keysBeingHovered     #returns a list of keys that are being hovered over
