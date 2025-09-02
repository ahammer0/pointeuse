from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from lib.DbAccess.DbAccess import DbAccess
from datetime import datetime


from lib.Periode.Duration import Duration
import lib.Periode.Periode as Periode

db = DbAccess()

app = Flask(__name__)
app.config["db"] = db


@app.route("/")
def hello_world():
    db: DbAccess = app.config["db"]
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes(10)
    currentPeriode = db.currentPeriode

    periodesbd = Periode.Periode.splitPeriodesAtMidnight(allPeriods)

    totalDuration: Duration = db.getTotalDurationSince(
        Periode.Periode.getMidnightTimestamp()
    )
    totalSinceMonday: Duration = db.getTotalDurationSince(
        Periode.Periode.getMondayMidnightTimestamp()
    )
    totalSinceFirstOfMonth: Duration = db.getTotalDurationSince(
        Periode.Periode.getFirstOfMonthTimestamp()
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

    totalDuration = db.getTotalDurationSince(Periode.Periode.getMidnightTimestamp())
    totalSinceMonday = db.getTotalDurationSince(
        Periode.Periode.getMondayMidnightTimestamp()
    )
    totalSinceFirstOfMonth = db.getTotalDurationSince(
        Periode.Periode.getFirstOfMonthTimestamp()
    )

    periodesbd = Periode.Periode.splitPeriodesAtMidnight(allPeriods)

    return (
        render_template(
            "status.html",
            jstate=state,
            currentPeriode=currentPeriode,
            periodes=allPeriods,
            totalTimestamp=totalDuration,
            totalSinceMonday=totalSinceMonday,
        )
        + render_template(
            "periodes.html",
            periodesbd=periodesbd,
            periodes=allPeriods,
            datetime=datetime,
        )
        + render_template(
            "dayTotal.html",
            currentPeriode=db.currentPeriode,
            totalTimestamp=totalDuration,
        )
        + render_template(
            "weekTotal.html",
            currentPeriode=db.currentPeriode,
            totalSinceMonday=totalSinceMonday,
        )
        + render_template(
            "monthTotal.html",
            currentPeriode=db.currentPeriode,
            totalSinceFirstOfMonth=totalSinceFirstOfMonth,
        )
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


@app.route("/periode", methods=["DELETE"])
def deletePeriode():
    db = app.config["db"]
    id = request.args.get("id")
    db.deletePeriode(id)
    return "", 200


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
    from lib.DbAccess import DbAccess

    db = DbAccess()
    webserver(db)
