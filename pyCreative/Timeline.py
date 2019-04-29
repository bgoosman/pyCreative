import TimeUtil
from Action import SimpleAction

class Timeline:
    def __init__(self):
        self.queued = []
        self.running = []

    def update(self):
        self.executeTriggeredActions()
        self.updateRunningActions()

    def executeTriggeredActions(self):
        for action in self.queued:
            if action.isTriggered():
                action.start()
                self.running.append(action)
        self.queued = [action for action in self.queued if not action.isTriggered()]

    def updateRunningActions(self):
        for action in self.running:
            action.update()
        self.running = [action for action in self.running if not action.isDone()]

    def clearScheduledActions(self):
        self.queued = []

    def cue(self, lambdaFunction=None, action=None):
        if lambdaFunction is not None:
            lambdaFunction()
        elif action is not None:
            self.running.append(action)
            action.start()

    def cueInSeconds(self, seconds: float, lambdaFunction=None, action=None):
        if lambdaFunction is not None:
            action = SimpleAction(lambdaFunction)
            action.triggerMicros = TimeUtil.getMicrosInFuture(seconds)
            self.queued.append(action)
        elif action is not None:
            action.triggerMicros = TimeUtil.getMicrosInFuture(seconds)
            self.queued.append(action)
