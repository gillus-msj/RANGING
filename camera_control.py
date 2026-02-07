import cv2 as cv
from picamera2 import Picamera2, Preview
from producer_thread import ProducerThread


class CameraControl(ProducerThread):
    
    def __init__(self, camera_id, window_name, window_offset):
        super().__init__()
        self.camera_id = camera_id
        self.window_name = window_name
        self.camera = self._configure_camera(camera_id)
        self.frame = None
        x_offset, y_offset = window_offset
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.moveWindow(window_name, x_offset, y_offset)
        self.camera.start()
            
    def _configure_camera(self, camera_id):
        camera = Picamera2(camera_id)
        preview_configuration = camera.create_preview_configuration()
        camera.configure(preview_configuration) 
        return camera
    
    def produce(self):
        if self.camera is not None:
            self.frame = self.camera.capture_array("main")
        return self.frame
    
    def set_overlay(self, frame, overlay_text):
        font = cv.FONT_HERSHEY_SIMPLEX
        font_size = 1
        font_color =(0, 0, 255)
        font_thickness = 1
        texte_pos = (25, 25)
        frame_out = cv.putText(frame, overlay_text, texte_pos, font, 
                                 font_size, font_color, font_thickness, cv.LINE_AA)
        return frame_out

    def display(self, overlay_text=None):
        if overlay_text:
            frame_overlayed = self.set_overlay(self.frame, overlay_text)
        else:
            frame_overlayed = self.frame
        cv.imshow(self.window_name, frame_overlayed)
    
    def close(self):
        self.camera.stop()

    def take_snapshot(self, name):
        #self.camera.capture_file(name + ".jpg")
        if self.frame is not None:
            cv.imwrite(name, self.frame)
