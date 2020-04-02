import time
import heapq
from functools import total_ordering

from pyCreative.Action import *
from pyCreative.MagicClass import *

class Beats:
    def __init__(self, beats):
        self.beats = beats

class Time:
    def __init__(self, seconds):
        self.seconds = seconds

class Seconds(Time):
    def __init__(self, seconds):
        Time.__init__(self, seconds)

@total_ordering
class ComparableAction:
    def __init__(self, seconds, action):
        self.action = action
        self.seconds = seconds

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return other.seconds == self.seconds

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return other.seconds > self.seconds

class MockTimeline(MagicClass):
    def __init__(self, ableton):
        MagicClass.__init__(self, 'MockTimeline')
        self.__dict__['timeline'] = []
        self.__dict__['ableton'] = ableton

    def cueIn(self, duration, action):
        if isinstance(duration, Beats):
            self.cueInSeconds(self.ableton.beatsToSeconds(duration.beats), action)
        elif isinstance(duration, Time):
            self.cueInSeconds(duration.seconds, action)
        else:
            print('Unknown type of duration {}'.format(str(duration)))

    def cueInSeconds(self, seconds, action):
        heapq.heappush(self.timeline, ComparableAction(seconds, action))

    def cueInBeats(self, beats, action):
        seconds = self.ableton.beatsToSeconds(beats)
        self.cueInSeconds(seconds, action)

    def isEmpty(self):
        return len(self.timeline) == 0

    def cueNextAction(self):
        comparableAction = heapq.heappop(self.timeline)
        self.cue(comparableAction.action)

    def cue(self, action):
        if callable(action):
            action()
        elif isinstance(action, ScheduledAction):
            if action.isCycleAction:
                return
            action.start()
        else:
            print('Unknown action type {}'.format(str(action)))

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
        self.queued = [action for action in self.queued if not action.running]

    def updateRunningActions(self):
        for action in self.running:
            action.update()
        self.running = [action for action in self.running if not action.isDone()]

    def clearScheduledActions(self):
        self.queued = []

    def clearRunningActions(self):
        self.running = []

    def wrap(self, action):
        # Wrap action in SimpleAction if is not already
        return SimpleAction(action) if callable(action) else action

    def cue(self, action):
        if callable(action):
            action()
        elif isinstance(action, ScheduledAction):
            self.running.append(action)
            action.start()
        else:
            print('Unknown action type {}'.format(str(action)))

    def cueIn(self, duration, action):
        if isinstance(action, SimpleAction) and action.isCycleAction:
            self.queued = [x for x in self.queued if not x.isCycleAction]
        if isinstance(duration, Beats):
            self.cueInBeats(duration.beats, action)
        elif isinstance(duration, Time):
            self.cueInSeconds(duration.seconds, action)
        else:
            print('Unknown type of duration {}'.format(str(duration)))

    def cueInSeconds(self, seconds: float, action):
        action = self.wrap(action)
        action.triggerInSeconds(seconds)
        self.queued.append(action)

    def cueInBeats(self, beats: int, action):
        action = self.wrap(action)
        action.triggerOnBeat(self.beat + beats)
        self.queued.append(action)
