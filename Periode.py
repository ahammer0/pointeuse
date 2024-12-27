import datetime

class Periode:
    def __init__(self, period):
        self.id = period[0]
        self.timestamp_in = period[1]
        self.timestamp_out = period[2]

    def __repr__(self):
        return f"Periode({self.id}, {self.timestamp_in}, {self.timestamp_out})"

    def getDuration(self):
        return Duration.fromPeriod(self)

class Duration:
    def __init__(self, duration): 
        self.duration = duration

    @classmethod
    def fromPeriod(cls, period):
        return cls(period.timestamp_out - period.timestamp_in)

    def getDurationStr(self):
        heure = int(self.duration / 3600)
        minute = int((self.duration % 3600) / 60)
        return f"{heure}h{minute}"

    def __repr__(self):
        return f"Duration({self.duration})"
    
    def __add__(self, other):
        if isinstance(other, Duration):
            return Duration(self.duration + other.duration)
        else:
            return self

    def __radd__(self, other):
        return self.__add__(other)

if __name__ == '__main__':
    p = Periode((1, 1735294708, 1735294708+120))
    print("doit donner 2 minutes")
