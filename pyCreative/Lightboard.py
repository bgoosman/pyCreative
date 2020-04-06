class Lightboard:
    def __init__(self):
        self.plot = dict()

    def update(self):
        pass

    def blackout(self):
        pass

    def setChannel(self, channel: int, value: int):
        pass

    def addFixture(self, name, fixture):
        self.plot[name] = fixture

    def getFixture(self, name):
        try:
            return self.plot[name]
        except KeyError:
            raise UnknownFixtureError(name)

class UnknownFixtureError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Unknown fixture "%s"' % self.name
