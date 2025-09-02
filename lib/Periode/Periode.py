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
        # sort periodes by day
        todayTs = Periode.getMidnightTimestamp()
        periodes_by_day: list[list[Periode]] = []

        retenue: Periode | None = None
        dayArr: list[Periode] = []
        for per in periodes:
            offset = len(periodes_by_day)
            mints = todayTs - offset * 24 * 60 * 60
            maxts = todayTs - (offset + 1) * 24 * 60 * 60

            if retenue is not None:
                dayArr.append(retenue)
                retenue = None

            if per.timestamp_out < mints:
                retenue = per
                periodes_by_day.append(dayArr)
                dayArr = []
                continue

            if per.timestamp_in < mints:
                retenue = Periode((per.id, per.timestamp_in, mints))
                toadd = Periode((per.id, mints, per.timestamp_out))
                dayArr.append(toadd)
                periodes_by_day.append(dayArr)
                dayArr = []
            else:
                dayArr.append(per)
        return periodes_by_day

    @staticmethod
    def getMondayMidnightTimestamp():
        date = datetime.datetime.now()
        while date.weekday() != 0:
            date = date - datetime.timedelta(days=1)
        date = date.replace(hour=0, minute=0, second=0)
        return int(date.timestamp())

    @staticmethod
    def getMidnightTimestamp():
        date = datetime.datetime.now()
        date = date.replace(hour=0, minute=0, second=0)
        return int(date.timestamp())

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
