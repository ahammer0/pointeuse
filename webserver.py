from flask import Flask
from flask import render_template
from flask import Response
from flask import request
from lib.DbAccess.DbAccess import DbAccess as DB
from datetime import datetime


from lib.Periode.Duration import Duration
import lib.Periode.Periode as Periode

db = DB()

app = Flask(__name__)
app.config["db"] = db


#######################
#   Routes standard   #
#######################
@app.route("/")
def hello_world():
    db: DB = app.config["db"]
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
        "pages/index.html",
        datetime=datetime,
        state=state,
        currentPeriode=currentPeriode,
        periodes=allPeriods,
        totalTimestamp=totalDuration,
        totalSinceMonday=totalSinceMonday,
        totalSinceFirstOfMonth=totalSinceFirstOfMonth,
        periodesbd=periodesbd,
    )


@app.route("/editperiode", methods=["GET"])
def editPeriod():
    db: DB = app.config["db"]
    id = request.args.get("id")

    if id is None:
        return "Id not provided", 400
    else:
        id = int(id)

    period = db.getPeriodeById(id)

    if period is None:
        return "Corresponding period not found", 404

    return render_template(
        "pages/edit_period_page.html",
        period=period,
    )


#######################
#   Routes API        #
#######################
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
            "components/status.html",
            jstate=state,
            currentPeriode=currentPeriode,
            periodes=allPeriods,
            totalTimestamp=totalDuration,
            totalSinceMonday=totalSinceMonday,
        )
        + render_template(
            "components/periodes.html",
            periodesbd=periodesbd,
            periodes=allPeriods,
            datetime=datetime,
        )
        + render_template(
            "components/dayTotal.html",
            currentPeriode=db.currentPeriode,
            totalTimestamp=totalDuration,
        )
        + render_template(
            "components/weekTotal.html",
            currentPeriode=db.currentPeriode,
            totalSinceMonday=totalSinceMonday,
        )
        + render_template(
            "components/monthTotal.html",
            currentPeriode=db.currentPeriode,
            totalSinceFirstOfMonth=totalSinceFirstOfMonth,
        )
    )


@app.route("/toggle", methods=["POST"])
def toggleWorking():
    db = app.config["db"]
    db.toggleWorking()
    return getStatus()


# @app.route("/periode", methods=["GET"])
# def getPeriode():
#     db = app.config["db"]
#     id = request.args.get("id")
#     if id is None:
#         periodes = db.getAllPeriodes()
#         return render_template("periodes.html", periodes=periodes)


@app.route("/periode", methods=["DELETE"])
def deletePeriode():
    db: DB = app.config["db"]
    id = request.args.get("id")
    db.deletePeriode(id)
    return "", 200


@app.route("/editperiode", methods=["POST"])
def editPeriode():
    db: DB = app.config["db"]
    date_str_in = request.form["ts_in"]
    date_str_out = request.form["ts_out"]
    id = request.form["id"]
    if date_str_in is None or date_str_out is None or id is None:
        return "Parameter missing", 400

    date_in = datetime.strptime(date_str_in, "%Y-%m-%dT%H:%M:%S")
    date_out = datetime.strptime(date_str_out, "%Y-%m-%dT%H:%M:%S")

    ts_in = int(date_in.timestamp())
    ts_out = int(date_out.timestamp())

    periode = Periode.Periode((int(id), int(ts_in), int(ts_out)))

    db.editPeriode(periode)
    return "", 200, {"HX-Redirect": "/"}


# @app.route("/getDayTotal", methods=["GET"])
# def getDayTotal():
#     db = app.config["db"]
#
#     date = datetime.now()
#     date = date.replace(hour=0, minute=0, second=0)
#     startOfDayTimestamp = int(date.timestamp())
#
#     totalDuration = db.getTotalDurationSince(startOfDayTimestamp)
#
#     return render_template(
#         "dayTotal.html",
#         totalTimestamp=totalDuration,
#         currentPeriode=db.currentPeriode,
#     )
#


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
