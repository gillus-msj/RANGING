# 
class Ranging:
    
    def __init__(self):
        ''' cameras parameters '''
        # Width of camera sensor, in pixels
        self.width_in_pix = 4444
        # Pixel Width, in mm
        self.pix_width = 0.02
        # Sensor width, in mm
        self.sensor_width = self.pix_width * self.width_in_pix
        # Focal length, unit = mm
        self.focal_length = 4
        
        ''' Integration parameters '''
        # Center distance of the two cameras, unit = mm
        self.focal_length = 100
        # Distance of convergence point of camera beams, in mm
        self.beam_convergence_distance = 10000
        
    def run(self, left, right):        

        
        return  True