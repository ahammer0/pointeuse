import datetime

from typing import List

from lib.Periode.Duration import Duration


class Periode:
    def __init__(self, period):
        self.id: int = period[0]
        self.timestamp_in: int = period[1]
        self.timestamp_out: int = period[2]

    def __str__(self):
        return f"Periode({self.id}, {self.timestamp_in}, {self.timestamp_out})"

    def __repr__(self):
        return f"Periode({self.id}, {self.getStartTimeStr()}, {self.getEndTimeStr()})"

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

    @classmethod
    def splitPeriodesAtMidnight(
        cls, periodes: List["Periode"]
    ) -> List[List["Periode"]]:
        """
        Split periodes into lists of periodes by day

        If a given period is ranging  from 11pm to 1 am, it will be split into 2 periods,
        one from 11pm to 12am and one from 12am to 1am
        """

        def splitPeriod(period: Periode) -> List[Periode]:
            mnIn = cls.getMidnightTimestamp(period.timestamp_in)
            mnOut = cls.getMidnightTimestamp(period.timestamp_out)

            if mnIn == mnOut:
                return [period]
            if mnOut > mnIn:
                return splitPeriod(
                    Periode((period.id, period.timestamp_in, mnOut - 1))
                ) + splitPeriod(Periode((period.id, mnOut, period.timestamp_out)))
            else:
                raise Exception("Period timestamp reverse !")

        splitPeriodes: List[Periode] = []
        for per in periodes:
            splitPeriodes += splitPeriod(per)
        splitPeriodes.sort(key=lambda per: per.timestamp_in, reverse=True)

        # sort periodes by day
        periodes_by_day: list[list[Periode]] = []
        dayPeriodes: List[Periode] = []

        curDayts = cls.getMidnightTimestamp(splitPeriodes[0].timestamp_in)
        for per in splitPeriodes:
            perDayTs = cls.getMidnightTimestamp(per.timestamp_in)
            if perDayTs == curDayts:
                dayPeriodes.append(per)
            else:
                periodes_by_day.append(dayPeriodes)
                dayPeriodes = []
                dayPeriodes.append(per)
                curDayts = cls.getMidnightTimestamp(per.timestamp_in)
        periodes_by_day.append(dayPeriodes)

        return periodes_by_day

    @staticmethod
    def getMondayMidnightTimestamp():
        date = datetime.datetime.now()
        while date.weekday() != 0:
            date = date - datetime.timedelta(days=1)
        date = date.replace(hour=0, minute=0, second=0)
        return int(date.timestamp())

    @staticmethod
    def getMidnightTimestamp(ts=None):
        if ts is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.fromtimestamp(ts)

        date = date.replace(hour=0, minute=0, second=0)
        return int(date.timestamp())

    @classmethod
    def getTodaySeconds(cls, ts: int):
        todayMidnight = cls.getMidnightTimestamp(ts)
        return ts - todayMidnight

    @staticmethod
    def getFirstOfMonthTimestamp():
        date = datetime.datetime.now()
        date = date.replace(day=1, hour=0, minute=0, second=0)
        return int(date.timestamp())


if __name__ == "__main__":
    p = Periode((1, 1735294708, 1735294708 + 120))
    print(p)
    repr(p)
    print("doit donner 2 minutes")
