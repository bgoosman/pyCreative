class MagicClass(object):
    def __init__(self, name):
        self.__dict__["name"] = name
        print(name)

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            wrapperName = "%s::%s" % (self.name, name)
            if len(args) > 0:
                wrapperName += "(%s)" % (",".join(map(lambda x: str(x), args)))
            return MagicClass(wrapperName)
        return wrapper

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self.log("%s=%s" % (name, value))

    def __getitem__(self, key):
        return key

    def __rtruediv__(self, other):
        return other

    def __rfloordiv__(self, other):
        return other

    def log(self, message):
        print("%s::%s" % (self.name, message))