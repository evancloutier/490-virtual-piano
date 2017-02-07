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
                if cv2.PointPolygonTest(cnt, point):
                    #get the corresponding key note from the contour
                    for key, value in keyDict.items():
                        if value == cnt:
                            keysBeingHovered,append(key)
        
        return keysBeingHovered     #returns a list of keys that are being hovered over