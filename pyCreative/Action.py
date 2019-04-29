import TimeUtil
import MathUtil

class ScheduledAction:
    def isTriggered(self):
        return TimeUtil.isInThePast(self.triggerMicros)

class SimpleAction(ScheduledAction):
    def __init__(self, lambdaFunction):
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
        self.durationMicros = TimeUtil.toMicros(durationSeconds)
        self.updateFunction = updateFunction
        self.min = min
        self.max = max

    def isDone(self):
        return TimeUtil.nowMicros() > self.endTime

    def start(self):
        self.startTime = TimeUtil.nowMicros()
        self.endTime = self.startTime + self.durationMicros

    def update(self):
        now = TimeUtil.nowMicros()
        value = MathUtil.map(now, self.startTime, self.endTime, self.min, self.max)
        self.updateFunction(value)
