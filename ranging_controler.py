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
LEFT_WINDOW_OFFSET = (10, 310) 
RIGHT_WINDOW_OFFSET = (510, 310) 
LEFT_MASK_WINDOW_OFFSET = (10, 660) 
RIGHT_MASK_WINDOW_OFFSET = (710, 660) 
CALIB_WINDOW_OFFSET = (10, 0) 
CALIB_WINDOW_SIZE = (900, 0) 
# Window names
LEFT_WINDOW_NAME = 'Left camera view'
RIGHT_WINDOW_NAME = 'Right camera view'
LEFT_MASK_WINDOW_NAME = 'Left Mask'
RIGHT_MASK_WINDOW_NAME = 'Right Mask'
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
        self.left_led_detection = LedDetection(LEFT_MASK_WINDOW_NAME, LEFT_MASK_WINDOW_OFFSET)
        self.right_led_detection = LedDetection(RIGHT_MASK_WINDOW_NAME, RIGHT_MASK_WINDOW_OFFSET)
        # Keep track of number of photo count to save them with incremented names
        self.photo_count = 0
        # Videa processing is done frame by frame, store current left & right frame under process
        self.display_mask = False
        self.gui_active = True

    def run(self):
        # Allow fps computation 
        fps = ComputeFps()
        # x,y position of target led 
        left_target, right_target = None, None
        # Start camera threads
        self.left_camera.start()
        self.right_camera.start()
        # Run while user doesn't request to stop
        while self._process_user_input():
            fps_text = f' fps: {fps()}'
            # Wait & Read the video frame by frame from both camera
            left_frame = self.left_camera.get()
            right_frame = self.right_camera.get()

            # Perform detection of led in frame
            left_position = self.left_led_detection.run(left_frame)
            right_position = self.right_led_detection.run(right_frame)

            # Perform ranging if we do have 2 cameras working
            self.ranging.run(left_position, right_position)

            # Display things only if gui_active
            if self.gui_active is True:
                # Show frame on screen
                self.left_camera.display(left_frame, fps_text)
                self.right_camera.display(right_frame, fps_text)

                # Display calibration scrollbars window, if requested
                if self.led_calibration:
                    self.led_calibration.show()

                # Display led detection mask frame, if requested
                if self.display_mask is True:
                    self.left_led_detection.display()
                    self.right_led_detection.display()
            # Print fps on terminal if no display on screen
            else:
                print(fps_text)

        # Terminate Camera threads
        self.left_camera.terminate()
        self.right_camera.terminate()
        
    def _process_user_input(self):
        go_on = True
        # Take commads from user
        cmd = cv.waitKey(1)
        if cmd & 0xFF == 255:
            return go_on
        if cmd & 0xFF == ord('g'):                
            if self.gui_active is False:
                # Display frames requested
                self.gui_active = True
            else:
                self.gui_active = False

        elif cmd & 0xFF == ord('c'):                
            if self.led_calibration is None:
                # Calibration requested
                self.led_calibration = LedCalibration(CALIBRATION_WINDOW_NAME, CALIB_WINDOW_SIZE, CALIB_WINDOW_OFFSET)
            else:
                self.led_calibration.hide()
                self.led_calibration = None
        
        elif cmd & 0xFF == ord('m'):                
            if self.display_mask is False:
                # Calibration requested
                self.left_led_detection.show()
                self.right_led_detection.show()
                self.display_mask = True
            else:
                self.left_led_detection.hide()
                self.right_led_detection.hide()
                self.display_mask = False

        elif cmd & 0xFF == ord('p'):
            # Take photo command, trigger one shot
            num = str(self.photo_count)
            cwd = os.getcwd()
            left_file_name = f"{cwd}/Left/left_{num}.jpg"
            right_file_name = f"{cwd}/Right/right_{num}.jpg"
            print(left_file_name)
            
            left_frame = self.left_camera.get()
            right_frame = self.right_camera.get()

            self.left_camera.take_snapshot(left_frame, left_file_name)
            self.right_camera.take_snapshot(right_frame, right_file_name)

            self.photo_count += 1 

        elif cmd & 0xFF == ord('q'):
            go_on = False
        return go_on

if __name__ == '__main__':

    ranging_control = RangingControler()
    ranging_control.run()
    cv.destroyAllWindows()
