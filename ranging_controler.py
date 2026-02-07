import os
import cv2 as cv

from camera_control import CameraControl
from led_calibration import LedCalibration
from led_detection import LedDetection
from ranging import Ranging
from compute_fps import ComputeFps


""" Local constants """
# Cam ID
LEFT_CAM_ID = 0
RIGHT_CAM_ID = 1

# Window width & hight offset
LEFT_WINDOW_OFFSET = (0, 0) 
RIGHT_WINDOW_OFFSET = (0, 700) 
MASK_WINDOW_OFFSET = (200, 200) 
CALIB_WINDOW_OFFSET = (200, 400) 
CALIB_WINDOW_SIZE = (700, 0) 
# Window names
LEFT_WINDOW_NAME = 'Left camera view'
RIGHT_WINDOW_NAME = 'Right camera view'
MASK_WINDOW_NAME = 'Mask'
CALIBRATION_WINDOW_NAME = ' Detection Calibration ' 


class RangingControler:
    
    def __init__(self):
    
        # Create separate threads to run video capture from each camera
        self.left_camera  = CameraControl(LEFT_CAM_ID, LEFT_WINDOW_NAME, LEFT_WINDOW_OFFSET)
        self.right_camera = CameraControl(RIGHT_CAM_ID, RIGHT_WINDOW_NAME, RIGHT_WINDOW_OFFSET)
        # Create the class taking care of depth computation from led positions
        self.ranging = Ranging()
        # Create reference to the class instntiated when led clibration is requested by user
        self.led_calibration = None
        # Create led detection class
        self.led_detection = LedDetection(MASK_WINDOW_NAME, MASK_WINDOW_OFFSET)
        # Keep track of number of photo count to save them with incremented names
        self.photo_count = 0
        # Videa processing is done frame by frame, store current left & right frame under process
        self.left_frame = None
        self.right_frame = None
        
    def run(self):
        # Allow fps computation 
        fps = ComputeFps()
        # x,y position of target led 
        left_target, right_target = None, None
        # Start camera threads
        self.left_camera.start()
        self.right_camera.start()
        # Run while user doesn't request to stop
        while self.process_user_input():
            fps_text = f' fps: {fps()}'
            # Wait & Read the video frame by frame from left camera
            self.left_frame = self.left_camera.get()
            if self.left_frame is not None:
                # Perform detection of led in frame
                left_target = self.led_detection.run(self.left_frame)
                # Show frame on screen
                self.left_camera.display(fps_text)
            # Wait & Read the video frame by frame from right camera
            self.right_frame = self.right_camera.get()
            if self.right_frame is not None:
                # Perform detection of led in frame
                right_target = self.led_detection.run(self.right_frame)
                # Show frame on screen
                self.right_camera.display(fps_text)
            # Perform ranging if we do have 2 cameras working
            if left_target and right_target:
                self.ranging.run(left_target, right_target)
            # Display calibration scrollbars window, if requested
            if self.led_calibration:
                self.led_calibration.show()
        # Terminate Camera threads
        self.left_camera.terminate()
        self.right_camera.terminate()
        
    def process_user_input(self):
        go_on = True
        # Take commads from user
        cmd = cv.waitKey(20)
        
        if cmd & 0xFF == ord('c'):                
            if self.led_calibration is None:
                # Calibration requested
                self.led_calibration = LedCalibration(CALIBRATION_WINDOW_NAME, CALIB_WINDOW_SIZE, CALIB_WINDOW_OFFSET)
            else:
                self.led_calibration.hide()
                self.led_calibration = None

        elif cmd & 0xFF == ord('p'):
            # Take photo command, trigger one shot
            num = str(self.photo_count)
            cwd = os.getcwd()
            left_file_name = f"{cwd}/Left/left_{num}.jpg"
            right_file_name = f"{cwd}/Right/right_{num}.jpg"
            print(left_file_name)
            
            self.left_camera.take_snapshot(left_file_name)
            self.right_camera.take_snapshot(right_file_name)

            self.photo_count += 1 

        elif cmd & 0xFF == ord('q'):
            go_on = False
        return go_on

if __name__ == '__main__':

    ranging_control = RangingControler()
    ranging_control.run()
    cv.destroyAllWindows()
