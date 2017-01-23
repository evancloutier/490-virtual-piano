import cv2
import imutils

class KeyDetector:

    def __init__(self):
        pass

        
    def receiveFrame(self, frame):
        self.data = frame.asarray()
        self.processFrame()
        
    def processFrame(self):
        blur = cv2.medianBlur(self.data, 37)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY)[1]
        
        #set data to whatever we want to return to imshow    
        self.data = thresh
        self.getOutsideRectangle()
        

    def transmitFrame(self):
        return self.data

    def getOutsideRectangle(self):
        
        #get contours
        cnts = cv2.findContours(self.data, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        cv2.drawContours(self.data, cnts[1], 0, [255,0,0], 2)
#        cv2.drawContours(self.data, cnts, -1, [255,0,0], 2)
        
        print(type(cnts))
        #epsilon marks accuracy of square
        #epsilon = 0.1*cv2.arcLength(cnts, True)
        #approx = cv2.approxPolyDP(cnts, epsilon, True)
        #(x, y, w, h) = cv2.boundingRect(approx)

        #cv2.rectangle(self.data, (x, y), (x + w + 100, y + h), (0, 255, 0), 2)

