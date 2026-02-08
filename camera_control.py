import cv2 as cv
from picamera2 import Picamera2, Preview
from producer_thread import ProducerThread


class CameraControl(ProducerThread):
    
    def __init__(self, camera_id, window_name, window_offset):
        super().__init__()
        self.camera_id = camera_id
        self.window_name = window_name
        self.camera = self._configure_camera(camera_id)
        x_offset, y_offset = window_offset
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.moveWindow(window_name, x_offset, y_offset)
        self.camera.start()
            
    def _configure_camera(self, camera_id):
        camera = Picamera2(camera_id)
        print("camera id :", camera_id, "sensor mode:", camera.sensor_modes)
        #preview_configuration = camera.create_preview_configuration(main={"size":(1536,864)}, queue=False)
        preview_configuration = camera.create_preview_configuration(main={"size":(640,480)}, queue=False)
        #preview_configuration = camera.create_preview_configuration(main={"size":(4608,2592)}, queue=False)
        camera.configure(preview_configuration)
        #camera.set_controls({"FrameRate": 30})
        #camera.set_controls({"FrameRate": 56.03})
        camera.set_controls({"FrameRate": 120.13})
        return camera
    
    def produce_(self):
        with self.camera.captured_request(flush=True) as request:
            frame = request.make_array("main")
        return frame
        
    def produce(self):
        return self.camera.capture_array("main")
    
    def _set_overlay(self, frame, overlay_text):
        font = cv.FONT_HERSHEY_SIMPLEX
        font_size = 1
        font_color =(0, 0, 255)
        font_thickness = 1
        texte_pos = (25, 25)
        return cv.putText(frame, overlay_text, texte_pos, font, 
                                 font_size, font_color, font_thickness, cv.LINE_AA)

    def display(self, frame, overlay_text=None):
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if overlay_text:
            frame_overlayed = self._set_overlay(frame, overlay_text)
        else:
            frame_overlayed = frame
        cv.imshow(self.window_name, frame_overlayed)
    
    def close(self):
        self.camera.stop()

    def take_snapshot(self, frame, name):
        #self.camera.capture_file(name + ".jpg")
        cv.imwrite(name, frame)
