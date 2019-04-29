import time

def nowMicros():
    return int(round(time.time() * 1e6))

def toMicros(seconds):
    return seconds * 1e6

def getMicrosInFuture(seconds):
    return int(nowMicros() + toMicros(seconds))

def isInThePast(triggerMicros):
    return triggerMicros < nowMicros()