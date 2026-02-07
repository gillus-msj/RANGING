import cv2 as cv
from PIL import Image

from led_calibration import H, S, V

class LedDetection:
    def __init__(self, window_name, window_offset):
        self.window_name = window_name
        self.window_offset = window_offset
        self.masked_frame = None


    def legit_leds(self, bbox):
        # Check that Height / width ratio should be around 4/1
        x1, y1, x2, y2 = bbox
        return True

    def run(self, frame):
        frame_color = (0, 255, 0)
        frame_width = 3
        # Convert frame to HSV (one-dimentional array) 
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        masked_frame = cv.inRange(hsv_frame, 
                                (H.low_value, S.low_value, V.low_value), 
                                (H.high_value, S.high_value, V.high_value))
        # Detect position of leds
        mask_image = Image.fromarray(masked_frame)
        bbox = mask_image.getbbox()
        if bbox is not None: 
            x1, y1, x2, y2 = bbox
            # Make sure that we capture the leds
            if self.legit_leds(bbox) is True:
                # Draw a frame aroud the leds
                frame = cv.rectangle(frame, (x1, y1), (x2, y2), frame_color, frame_width)
                masked_frame = cv.rectangle(masked_frame, (x1, y1), (x2, y2), frame_color, frame_width)
                self.masked_frame = masked_frame
        return True, bbox
    
    def display(self):
        if self.masked_frame is not None:
            cv.imshow(self.window_name, self.masked_frame)

    def show(self):
        x, y = self.window_offset
        cv.namedWindow(self.window_name)
        cv.moveWindow(self.window_name, x, y)
        cv.destroyWindow(self.window_name)

    def hide(self):
        cv.destroyWindow(self.window_name)



