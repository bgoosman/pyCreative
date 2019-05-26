from pyCreative import TimeUtil
from pyCreative import MathUtil

class ScheduledAction:
    def __init__(self):
        self.triggerBeat = None
        self.triggerTime = None

    def triggerOnBeat(self, beat):
        self.triggerBeat = beat

    def triggerInSeconds(self, seconds):
        self.triggerTime = TimeUtil.now() + seconds

    def isTriggered(self, currentBeat):
        if self.triggerTime is not None:
            return self.triggerTime < TimeUtil.now()
        elif self.triggerBeat is not None:
            return self.triggerBeat <= currentBeat

class SimpleAction(ScheduledAction):
    def __init__(self, lambdaFunction):
        ScheduledAction.__init__(self)
        self.lambdaFunction = lambdaFunction

    def isDone(self):
        return True

    def start(self):
        self.lambdaFunction()

    def update(self):
        pass

class LerpAction(ScheduledAction):
    def __init__(self, durationSeconds, updateFunction, min, max):
        self.startTime = None
        self.endTime = None
        self.duration = durationSeconds
        self.updateFunction = updateFunction
        self.min = min
        self.max = max

    def isDone(self):
        return TimeUtil.now() > self.endTime

    def start(self):
        self.startTime = TimeUtil.now()
        self.endTime = self.startTime + self.duration

    def update(self):
        value = MathUtil.map(TimeUtil.now(), self.startTime, self.endTime, self.min, self.max)
        self.updateFunction(value)
