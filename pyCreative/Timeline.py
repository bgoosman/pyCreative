import time

from pyCreative.Action import SimpleAction

class Timeline:
    def __init__(self, ableton):
        self.ableton = ableton
        self.ableton.addBeatCallback(self.onBeat)
        self.queued = []
        self.running = []
        self.updatesPerSecond = 30
        self.secondsPerUpdate = 1.0 / self.updatesPerSecond
        self.nextUpdate = time.time() + self.secondsPerUpdate
        self.beat = 0

    def onBeat(self, beat):
        self.beat = beat
        self.executeTriggeredActions()

    def update(self):
        now = time.time()
        if now > self.nextUpdate:
            self.executeTriggeredActions()
            self.updateRunningActions()
            self.nextUpdate = now + self.secondsPerUpdate

    def stop(self):
        self.clearScheduledActions()
        self.clearRunningActions()

    def cleanup(self):
        self.clearScheduledActions()

    def executeTriggeredActions(self):
        for action in self.queued:
            if action.isTriggered(self.beat):
                action.start()
                self.running.append(action)
        self.queued = [action for action in self.queued if not action.isTriggered(self.beat)]

    def updateRunningActions(self):
        for action in self.running:
            action.update()
        self.running = [action for action in self.running if not action.isDone()]

    def clearScheduledActions(self):
        self.queued = []

    def clearRunningActions(self):
        self.running = []

    def cue(self, f=None, action=None):
        if f is not None:
            f()
        elif action is not None:
            self.running.append(action)
            action.start()

    def cueInSeconds(self, seconds: float, f=None, action=None):
        if f is not None:
            action = SimpleAction(f)
            action.triggerInSeconds(seconds)
            self.queued.append(action)
        elif action is not None:
            action.triggerInSeconds(seconds)
            self.queued.append(action)

    def cueInBeats(self, beats: int, f=None, action=None):
        if f is not None:
            action = SimpleAction(f)
            action.triggerOnBeat(self.beat + beats)
            self.queued.append(action)
        elif action is not None:
            action.triggerOnBeat(self.beat + beats)
            self.queued.append(action)
