from dmxpy import DmxPy

MAX_VALUE = 255

class DmxLightBoard:
    def __init__(self, serialPort):
        self.dmx = DmxPy.DmxPy(serialPort)
        self.fixtures = []
        self.dirty = False

    def update(self):
        if self.dirty:
            self.dmx.render()
            self.dirty = False

    def setChannel(self, channel: int, value: int):
        self.dirty = True
        self.dmx.setChannel(channel, value)

    def blackout(self):
        self.dmx.blackout()

class ChauvetOvationE910FC:
    def __init__(self, dmx: DmxLightBoard, startChannel: int = 0,
                 dimmer: int = 0, red: int = 0, green: int = 0, blue: int = 0, amber: int = 0):
        self.dmx = dmx
        self.startChannel = startChannel
        self._dimmer = dimmer
        self._red = red
        self._green = green
        self._blue = blue
        self._amber = amber

    def values(self):
        return [self._dimmer, self._red, self._green, self._blue, self._amber]

    @property
    def dimmer(self):
        return self._dimmer

    @dimmer.setter
    def dimmer(self, value):
        if value in range(0, MAX_VALUE+1):
            self._dimmer = value
            self.dmx.setChannel(self.startChannel, value)

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        if value in range(0, MAX_VALUE+1):
            self._red = value
            self.dmx.setChannel(self.startChannel+1, value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        if value in range(0, MAX_VALUE+1):
            self._green = value
            self.dmx.setChannel(self.startChannel+2, value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        if value in range(0, MAX_VALUE+1):
            self._blue = value
            self.dmx.setChannel(self.startChannel+3, value)

    @property
    def amber(self):
        return self._amber

    @amber.setter
    def amber(self, value):
        if value in range(0, MAX_VALUE+1):
            self._amber = value
            self.dmx.setChannel(self.startChannel+4, value)
