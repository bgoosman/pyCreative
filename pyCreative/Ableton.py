import LinkToPy
import live
import threading
import time

class Ableton(threading.Thread):
    MAX_FILTER_FREQUENCY = 135
    MIN_FILTER_FREQUENCY = 20
    ZERO_DB = 0.88

    def __init__(self):
        threading.Thread.__init__(self)
        self.link = LinkToPy.LinkInterface('/Applications/Carabiner')
        self.set = live.Set()
        try:
            self.set.load()
        except Exception as e:
            print(str(e))
            self.scan()
        self.zeroAllTrackVolumes()
        self.stopAllClips()
        self.running = True

    def run(self):
        while self.running:
            self.link.update_status()
            time.sleep(0.075)

    def cleanup(self):
        self.running = False
        self.link.cleanup()
        self.stop()

    def scan(self):
        self.set.scan(group_re='=.+', scan_clip_names=True, scan_devices=True)

    def get_status(self):
        return self.link.get_status_string()

    def play(self):
        self.set.play()
        self.link.play()

    def stop(self):
        self.set.stop()
        self.link.stop()

    def mute(self):
        self.getTrack('Master').volume = 0

    def tracks(self):
        return self.set.tracks

    def bpm(self):
        return self.link.bpm_

    def setBpm(self, bpm):
        self.link.set_bpm(bpm)

    def waitForNextBeat(self):
        self.set.wait_for_next_beat()

    def getGroup(self, name):
        return self.set.get_group(name)

    def getTrack(self, name):
        return self.set.get_track(name)

    def addBeatCallback(self, callback):
        self.link.add_beat_callback(callback)

    def zeroAllTrackVolumes(self):
        for track in self.set.tracks:
            track.volume = Ableton.ZERO_DB

    def playClip(self, name):
        track = self.set.get_track(name)
        if track:
            track.play_clip(name=name)

    def stopAllClips(self):
        for track in self.set.tracks:
            for clip in filter(lambda x: x is not None, track.clips):
                clip.stop()

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

    def beatsToSeconds(self, beats):
        return beats * (1.0 / self.bpm()) * 60.0

    def millisecondsPerBeat(self, bpm=None):
        if bpm is None:
            bpm = self.bpm()
        return 1.0 / (bpm / 60.0) * 1000.0

    def clampFilterFrequency(self, frequency):
        if frequency < 20:
            return 20
        elif frequency > 135:
            return 135
        else:
            return frequency

    def __del__(self):
        self.set.stop()
        del self.link
