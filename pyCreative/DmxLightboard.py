from dmxpy import DmxPy

class DmxLightboard:
    MAX_VALUE = 255

    def __init__(self, serialPort):
        self.dmx = DmxPy.DmxPy(serialPort)
        self.fixtures = []
        self.dirty = False

    def update(self):
        if self.dirty:
            self.dmx.render()
            self.dirty = False

    def setChannel(self, channel: int, value: int):
        # print('setChannel {} @ {}'.format(channel, value))
        self.dirty = True
        self.dmx.setChannel(channel, value)

    def blackout(self):
        self.dirty = True
        self.dmx.blackout()

    def cleanup(self):
        self.dmx.close()

class GenericDmxFixture:
    def blackout(self):
        self.set(len(self.values()) * [0])

    def fractional(self, value):
        self.set(len(self.values()) * [int(DmxLightboard.MAX_VALUE * value)])

    def fullOn(self):
        self.set(len(self.values()) * [DmxLightboard.MAX_VALUE])

class Par38(GenericDmxFixture):
    def __init__(self, dmx: DmxLightboard, startChannel: int = 0, red: int = 0, green: int = 0, blue: int = 0):
        self.dmx = dmx
        self.startChannel = startChannel
        self.red = red
        self.green = green
        self.blue = blue

    def values(self):
        return [self._red, self._green, self._blue]

    def set(self, values):
        self.red = values[0]
        self.green = values[1]
        self.blue = values[2]

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._red = value
            self.dmx.setChannel(self.startChannel, value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._green = value
            self.dmx.setChannel(self.startChannel+1, value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._blue = value
            self.dmx.setChannel(self.startChannel+1, value)

class Par64(GenericDmxFixture):
    def __init__(self, dmx: DmxLightboard, startChannel: int = 0, red: int = 0, green: int = 0, blue: int = 0):
        self.dmx = dmx
        self.startChannel = startChannel
        self.red = red
        self.green = green
        self.blue = blue

    def values(self):
        return [self._red, self._green, self._blue]

    def set(self, values):
        self.red = values[0]
        self.green = values[1]
        self.blue = values[2]

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._red = value
            self.dmx.setChannel(self.startChannel, value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._green = value
            self.dmx.setChannel(self.startChannel+1, value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._blue = value
            self.dmx.setChannel(self.startChannel+1, value)

class ChauvetOvationE910FC(GenericDmxFixture):
    def __init__(self, dmx: DmxLightboard, startChannel: int = 0,
                 dimmer: int = 0, red: int = 0, green: int = 0, blue: int = 0, amber: int = 0):
        self.dmx = dmx
        self.startChannel = startChannel
        self.dimmer = dimmer
        self.red = red
        self.green = green
        self.blue = blue
        self.amber = amber

    def values(self):
        return [self._dimmer, self._red, self._green, self._blue, self._amber]

    def set(self, values):
        self.dimmer = values[0]
        self.red = values[1]
        self.green = values[2]
        self.blue = values[3]
        self.amber = values[4]

    @property
    def dimmer(self):
        return self._dimmer

    @dimmer.setter
    def dimmer(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._dimmer = value
            self.dmx.setChannel(self.startChannel, value)

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._red = value
            self.dmx.setChannel(self.startChannel+1, value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._green = value
            self.dmx.setChannel(self.startChannel+2, value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._blue = value
            self.dmx.setChannel(self.startChannel+3, value)

    @property
    def amber(self):
        return self._amber

    @amber.setter
    def amber(self, value):
        if value in range(0, DmxLightboard.MAX_VALUE+1):
            self._amber = value
            self.dmx.setChannel(self.startChannel+4, value)
