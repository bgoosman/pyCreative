from pyCreative import TimeUtil
from pyCreative import MathUtil

class ScheduledAction:
    def __init__(self):
        self.triggerBeat = None
        self.triggerTime = None
        self.isCycleAction = False
        self.running = False

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
        self.running = True
        self.lambdaFunction()

    def update(self):
        pass

class InstantLerpAction(ScheduledAction):
    def __init__(self, updateFunction, min, max):
        ScheduledAction.__init__(self)
        self.updateFunction = updateFunction
        self.min = min
        self.max = max
        self.step = 0.01

    def start(self):
        self.updateFunction(self.min)
        self.updateFunction(self.max)

class LerpAction(ScheduledAction):
    def __init__(self, durationSeconds, updateFunction, min, max):
        ScheduledAction.__init__(self)
        self.isCycleAction = False
        self.startTime = None
        self.endTime = None
        self.duration = durationSeconds
        self.updateFunction = updateFunction
        self.min = min
        self.max = max
        self.running = False

    def isDone(self):
        return TimeUtil.now() > self.endTime

    def start(self):
        self.running = True
        self.startTime = TimeUtil.now()
        self.endTime = self.startTime + self.duration

    def update(self):
        value = MathUtil.map(TimeUtil.now(), self.startTime, self.endTime, self.min, self.max)
        self.updateFunction(value)
