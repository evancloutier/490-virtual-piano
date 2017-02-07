import cv2

class FingerMapper:
    def __init__(self):
        pass
    
    def getKeysBeingHovered(self, fingerPoints, keyContours, keyDict):
        keysBeingHovered = []
        
        #we want to reference the fingerPoints with the area of the keyContours
        
        for cnt in keyContours:
            for point in fingerPoints:
                #check if point in key contour
                #keep track of how many fingers are in a contour
                fingerCount = 0;
                if cv2.PointPolygonTest(cnt, point):
                    #get the corresponding key note from the contour
                    for key, value in keyDict.items():
                        if value == cnt and fingerCount == 0:
                        x    keysBeingHovered,append(key)
                        fingerCount = fingerCount + 1
        
        return keysBeingHovered     #returns a list of keys that are being hovered over