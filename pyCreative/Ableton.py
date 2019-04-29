import LinkToPy
import live

class Ableton:
    def __init__(self):
        self.link = LinkToPy.LinkInterface('/Applications/Carabiner')
        self.set = live.Set()
        self.set.scan(scan_clip_names=True, scan_devices=True)

    def update(self):
        self.link.update_status()

    def get_status(self):
        return self.link.get_status_string()

    def play(self):
        self.set.play()

    def stop(self):
        self.set.stop()

    def waitForNextBeat(self):
        self.set.wait_for_next_beat()

    def getTrack(self, trackName):
        return self.set.get_track(trackName)

    def playClip(self, trackName, clipName):
        clip = self.set.get_clip(trackName, clipName)
        if clip:
            clip.play()

    def stopClip(self, trackName, clipName):
        clip = self.set.get_clip(trackName, clipName)
        if clip:
            clip.stop()

    def setParameter(self, trackName, deviceName, parameterName, value):
        track = self.set.get_track(trackName)
        if track:
            device = track.get_device(deviceName)
            if device:
                parameter = device.get_parameter_by_name(parameterName)
                if parameter:
                    parameter.value = value

    def __del__(self):
        self.set.stop()
        del self.link
