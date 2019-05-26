import threading
import cv2

class VideoBuffer(threading.Thread):
    def __init__(self, capture, max_frames):
        threading.Thread.__init__(self)
        self.capture = capture
        self.frames = [None for x in range(max_frames)]
        self.index = 0
        self.max_frames = max_frames
        self.frames_lock = threading.Lock()
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            with self.frames_lock:
                self.frames[self.index] = frame
                self.index += 1
                if self.index == self.max_frames:
                    self.index = 0

    def get_max_fps(self):
        return self.capture.get(cv2.CAP_PROP_FPS)

    def get(self, index):
        if 0 <= index and index < self.max_frames:
            with self.frames_lock:
                return self.frames[index]
        return None

    def get_last(self):
        last_index = self.index - 1
        if last_index < 0:
            last_index = self.max_frames - 1
        with self.frames_lock:
            return self.frames[last_index]

    def cleanup(self):
        self.running = False

    def __len__(self):
        return self.max_frames
