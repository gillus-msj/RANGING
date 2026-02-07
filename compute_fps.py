from time import time_ns

class ComputeFps:
    ''' Compute number of frames per second '''
    def __init__(self):
        self.fps = 0
        self.nb_frames = 0
        self.start_time = time_ns()

    def __call__(self):
        ''' Should be called at each new frame, return fps '''
        self.nb_frames = self.nb_frames + 1
        current_time = time_ns()
        if current_time - self.start_time >= 1000000000:
            self.start_time = current_time
            self.fps = self.nb_frames
            self.nb_frames = 0
        return self.fps

