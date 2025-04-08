import datetime
import time


class Periode:
    def __init__(self, period):
        self.id: int = period[0]
        self.timestamp_in: int = period[1]
        self.timestamp_out: int = period[2]

    def __str__(self):
        return f"Periode({self.id}, {self.timestamp_in}, {self.timestamp_out})"

    def getStartTimeStr(self):
        return datetime.datetime.fromtimestamp(self.timestamp_in).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def getEndTimeStr(self):
        if self.timestamp_out is None:
            return "En cours"
        return datetime.datetime.fromtimestamp(self.timestamp_out).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def getDuration(self):
        return Duration.fromPeriod(self)


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


if __name__ == "__main__":
    p = Periode((1, 1735294708, 1735294708 + 120))
    print(p)
    repr(p)
    print("doit donner 2 minutes")
