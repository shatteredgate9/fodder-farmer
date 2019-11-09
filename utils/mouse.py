import cv2 as cv

class Mouse:
    def initMouseTracking(self, windowName):
        cv.setMouseCallback(windowName, self.on_mouse_move, cv.EVENT_MOUSEMOVE)  
        
    def on_mouse_move(self, eventName, x, y, flags, userdata):
        print(x, y)
        if eventName == cv.EVENT_MOUSEMOVE:
            print(x, y)
    
