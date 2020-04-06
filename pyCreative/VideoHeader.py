from PyQt5.QtCore import *

class VideoHeader:
    def __init__(self, videoBuffer):
        self.videoBuffer = videoBuffer
        self.index = videoBuffer.index
        self.timer = None

    def getLast(self):
        return self.videoBuffer.get_last()

    def getHead(self):
        return self.videoBuffer.get(self.index)

    def setDelaySeconds(self, seconds):
        frames = int(self.videoBuffer.get_max_fps() * seconds)
        self.index = self.videoBuffer.index - frames
        if self.index < 0:
            self.index = len(self.videoBuffer) + self.index

    def advance(self):
        nextIndex = self.index + 1
        if nextIndex == len(self.videoBuffer):
            nextIndex = 0
        if self.videoBuffer.get(nextIndex) is not None:
            self.index = nextIndex

    def start(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        self.index = self.videoBuffer.index
        self.timer = QTimer()
        self.timer.timeout.connect(self.advance)
        self.timer.start(1000.0 / self.videoBuffer.get_max_fps())

    def stop(self):
        if self.timer:
            self.timer.stop()
