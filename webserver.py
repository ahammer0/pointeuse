from flask import Flask
from flask import render_template
from flask import Response
from DbAccess import DbAccess
from datetime import datetime
from datetime import timedelta

from Periode import Duration
import Periode

db = DbAccess()

app = Flask(__name__)
app.config["db"] = db


def getMondayMidnightTimestamp():
    date = datetime.now()
    while date.weekday() != 0:
        date = date - timedelta(days=1)
    date = date.replace(hour=0, minute=0, second=0)
    return int(date.timestamp())


def getMidnightTimestamp():
    date = datetime.now()
    date = date.replace(hour=0, minute=0, second=0)
    return int(date.timestamp())


def getFirstOfMonthTimestamp():
    date = datetime.now()
    date = date.replace(day=1, hour=0, minute=0, second=0)
    return int(date.timestamp())


@app.route("/")
def hello_world():
    db: DbAccess = app.config["db"]
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes(10)
    currentPeriode = db.currentPeriode

    periodesbd: list[list[Periode.Periode]] = []
    # sort periodes by day
    todayTs = getMidnightTimestamp()

    retenue: Periode.Periode | None = None
    dayArr: list[Periode.Periode] = []
    for per in allPeriods:
        offset = len(periodesbd)
        mints = todayTs - offset * 24 * 60 * 60
        maxts = todayTs - (offset + 1) * 24 * 60 * 60

        if retenue is not None:
            dayArr.append(retenue)
            retenue = None

        if per.timestamp_out < mints:
            retenue = per
            periodesbd.append(dayArr)
            dayArr = []
            continue

        if per.timestamp_in < mints:
            retenue = Periode.Periode((per.id, per.timestamp_in, mints))
            toadd = Periode.Periode((per.id, mints, per.timestamp_out))
            dayArr.append(toadd)
            periodesbd.append(dayArr)
            dayArr = []
        else:
            dayArr.append(per)

    totalDuration: Duration = db.getTotalDurationSince(getMidnightTimestamp())
    totalSinceMonday: Duration = db.getTotalDurationSince(getMondayMidnightTimestamp())
    totalSinceFirstOfMonth: Duration = db.getTotalDurationSince(
        getFirstOfMonthTimestamp()
    )

    return render_template(
        "index.html",
        datetime=datetime,
        state=state,
        currentPeriode=currentPeriode,
        periodes=allPeriods,
        totalTimestamp=totalDuration,
        totalSinceMonday=totalSinceMonday,
        totalSinceFirstOfMonth=totalSinceFirstOfMonth,
        periodesbd=periodesbd,
    )


@app.route("/getStatus", methods=["GET"])
def getStatus():
    db = app.config["db"]
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes()
    currentPeriode = db.currentPeriode

    totalDuration = db.getTotalDurationSince(getMidnightTimestamp())
    totalSinceMonday = db.getTotalDurationSince(getMondayMidnightTimestamp())

    return render_template(
        "status.html",
        isUpdate=True,
        jstate=state,
        currentPeriode=currentPeriode,
        periodes=allPeriods,
        totalTimestamp=totalDuration,
        totalSinceMonday=totalSinceMonday,
    )


@app.route("/toggle", methods=["POST"])
def toggleWorking():
    db = app.config["db"]
    db.toggleWorking()
    return getStatus()


@app.route("/getPeriodes", methods=["GET"])
def getPeriodes():
    db = app.config["db"]
    periodes = db.getAllPeriodes()
    return render_template("periodes.html", periodes=periodes)


@app.route("/getDayTotal", methods=["GET"])
def getDayTotal():
    db = app.config["db"]

    date = datetime.now()
    date = date.replace(hour=0, minute=0, second=0)
    startOfDayTimestamp = int(date.timestamp())

    totalDuration = db.getTotalDurationSince(startOfDayTimestamp)

    return render_template(
        "dayTotal.html",
        totalTimestamp=totalDuration,
        currentPeriode=db.currentPeriode,
    )


@app.route("/stream")
def events():
    db = app.config["db"]

    def SSE():
        yield "event: init\ndata: init\n\n"
        while True:
            status = db.waitChangedFlag()
            yield f"event: newdata\ndata: newdatadata {status}\n\n"
            print("\nsse newdata sent")

    return Response(SSE(), mimetype="text/event-stream")


def webserver(db):
    app.config["db"] = db
    app.run(host="0.0.0.0", port=5000, threaded=True)


if __name__ == "__main__":
    print("test webserver")
    from DbAccess import DbAccess

    db = DbAccess()
    webserver(db)
