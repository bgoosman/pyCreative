from pyCreative.VideoBuffer import *
from pyCreative.VideoHeader import *
from pyCreative.MagicClass import *

class MockVideoStream(MagicClass):
    def __init__(self, name, frame):
        MagicClass.__init__(self, name)
        self.__dict__['frame'] = frame

    def getHead(self):
        self.log('getHead')
        return self.frame

    def getLast(self):
        self.log('getLast')
        return self.frame

class VideoStream:
    def __init__(self, videoCapture):
        self.videoCapture = videoCapture
        self.videoBuffer = VideoBuffer(videoCapture, 300)
        self.videoBuffer.start()
        self.videoHeader = VideoHeader(self.videoBuffer)

    def start(self):
        self.videoHeader.start()

    def getMaxFps(self):
        return self.videoBuffer.get_max_fps()

    def getLast(self):
        return self.videoBuffer.get_last()

    def getHead(self):
        return self.videoHeader.getHead()

    def setDelaySeconds(self, seconds):
        self.videoHeader.setDelaySeconds(seconds)

    def cleanup(self):
        self.videoHeader.stop()
        self.videoBuffer.cleanup()
        self.videoBuffer.join()
        self.videoCapture.release()
