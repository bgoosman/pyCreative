import threading
import time
import cv2

class VideoBuffer(threading.Thread):
    def __init__(self, capture, max_frames, read_fps=None):
        threading.Thread.__init__(self)
        self.capture = capture
        self.frames = [None for x in range(max_frames)]
        self.index = 0
        self.max_frames = max_frames
        self.frames_lock = threading.Lock()
        self.running = True
        self.read_fps = read_fps
        self.last_read = None
        self.number_of_reads = 0
        self.sum_of_read_times = 0
        self.average_fps = 0

    def compute_fps(self):
        now = time.time()
        if self.last_read is not None:
            read_time = now - self.last_read
            self.sum_of_read_times += read_time
            self.number_of_reads += 1
            self.average_fps = 1 / (self.sum_of_read_times / self.number_of_reads)
        self.last_read = now

    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            self.compute_fps()
            with self.frames_lock:
                self.frames[self.index] = frame
                self.index += 1
                if self.index == self.max_frames:
                    self.index = 0
            if self.read_fps is not None:
                time.sleep(1.0 / self.read_fps)

    def get_average_fps(self):
        return self.average_fps

    def get_max_fps(self):
        if self.read_fps is not None:
            return self.read_fps
        else:
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
