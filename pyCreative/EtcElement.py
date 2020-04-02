import liblo
from pyCreative.Action import *

def ignoreOsError(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except OSError:
            pass
    return inner

class EtcElement:
    CHANNEL_MIN = 0
    CHANNEL_MAX = 120
    VALUE_MIN = 0
    VALUE_MAX = 100

    def __init__(self, remoteIp, remotePort):
        self.oscTarget = liblo.Address(remoteIp, remotePort)

    @ignoreOsError
    def setChannel(self, channel, level):
        message = '/eos/chan/{}'.format(channel)
        liblo.send(self.oscTarget, message, level)

    def fadeChannel(self, channel, durationSeconds, startLevel, endLevel):
        def updateFunction(value):
            value = int(value)
            self.setChannel(channel, value)
        return LerpAction(durationSeconds, updateFunction, startLevel, endLevel)

    def update(self):
        pass

    def blackout(self):
        for i in range(EtcElement.CHANNEL_MAX):
            self.setChannel(i, 0)
