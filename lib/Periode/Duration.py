import time


class Duration:
    def __init__(self, duration):
        if duration is None:
            self.duration = 0
        else:
            self.duration = duration

    @classmethod
    def fromPeriod(cls, period):
        if period.timestamp_out is None:
            return cls(int(time.time()) - period.timestamp_in)
        return cls(period.timestamp_out - period.timestamp_in)

    def __str__(self):
        heure = int(self.duration / 3600)
        minute = int((self.duration % 3600) / 60)
        secondes = int((self.duration % 3600) % 60)
        return f"{heure}h{minute}m{secondes}s"

    def toTimestamp(self):
        return int(self.duration)

    def __add__(self, other):
        if isinstance(other, Duration):
            return Duration(self.duration + other.duration)
        else:
            return self

    def __radd__(self, other):
        return self.__add__(other)
