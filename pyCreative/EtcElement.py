import liblo

def ignoreOsError(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except OSError:
            pass
    return inner

class EtcElement:
    def __init__(self, remoteIp, remotePort):
        self.oscTarget = liblo.Address(remoteIp, remotePort)
        self.channelMin = 0
        self.channelMax = 120
        self.lightMin = 0
        self.lightMax = 100

    @ignoreOsError
    def setChannel(self, channel, level):
        message = '/eos/chan/{}'.format(channel)
        liblo.send(self.oscTarget, message, level)

    def update(self):
        pass

    def blackout(self):
        for i in range(self.channelMax):
            self.setChannel(i, 0)
