import cv2 as cv
import numpy as np

class Axe:
    window_name = None
    
class H(Axe):
    name = 'H'
    min_value = 0
    max_value = 180
    low_value = 120
    high_value = 124
         
class S(Axe):
    name = 'S'
    min_value = 0
    max_value = 255
    low_value = 251
    high_value = 255 

class V(Axe):
    name = 'V'
    min_value = 0
    max_value = 255
    low_value = 254
    high_value = 255  
    
class LedCalibration:

    def __init__(self, window_name,  window_size, window_offset):
        self.window_name = window_name
        self.window_size = window_size
        x_offset, y_offset = window_offset
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.moveWindow(window_name, x_offset, y_offset)  
        Axe.window_name = window_name    
        self.create_trackbar(H)
        self.create_trackbar(S)
        self.create_trackbar(V)
        
    def create_trackbar(self, axe):
        cv.createTrackbar(axe.name + '_low', axe.window_name, axe.low_value, axe.max_value, 
                          lambda value: self.on_low_change(axe, value))
        cv.createTrackbar(axe.name + '_high', axe.window_name, axe.high_value, axe.max_value, 
                          lambda value: self.on_high_change(axe, value))
        
    @staticmethod
    def on_low_change(axe, value):
        axe.low_value = min(axe.high_value - 1, value)
        if value > axe.low_value:
            cv.setTrackbarPos(axe.name + '_low', axe.window_name, axe.low_value)
        
    @staticmethod  
    def on_high_change(axe, value):
        axe.high_value = max(value, axe.low_value + 1)
        if value < axe.high_value:
            cv.setTrackbarPos(axe.name + '_high', axe.window_name, axe.high_value)

    def show(self):
        window_name = self.window_name
        for axe in (H, S, V):
            name = axe.name + '_low'
            value = cv.getTrackbarPos(name, window_name)
            if value > axe.low_value:
                cv.setTrackbarPos(name, window_name, axe.low_value)
            name = axe.name + '_high'
            value = cv.getTrackbarPos(name, window_name)
            if value < axe.high_value:
                cv.setTrackbarPos(name, window_name, axe.low_value)
        x, y = self.window_size
        empty_frame = np.uint8([[0,255,0]])
        cv.imshow(self.window_name, empty_frame)
        cv.resizeWindow(self.window_name, x, y)
        
    def hide(self):
        cv.destroyWindow(self.window_name)
