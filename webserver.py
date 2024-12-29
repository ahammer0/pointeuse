from flask import Flask
from flask import render_template
from flask import Response
from DbAccess import DbAccess
from datetime import datetime
from datetime import timedelta
db = DbAccess()

app = Flask(__name__)
app.config['db'] = db

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

@app.route('/')
def hello_world():
    db = app.config['db']
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes()
    currentPeriode = db.currentPeriode

    totalDuration = db.getTotalDurationSince(getMidnightTimestamp())
    totalSinceMonday = db.getTotalDurationSince(getMondayMidnightTimestamp())   

    return render_template('index.html',
        state=state,
        currentPeriode=currentPeriode,
        periodes=allPeriods,
        totalTimestamp=totalDuration,
        totalSinceMonday=totalSinceMonday)

@app.route('/getStatus', methods=['GET'])
def getStatus():
    db = app.config['db']
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes()
    currentPeriode = db.currentPeriode

    totalDuration = db.getTotalDurationSince(getMidnightTimestamp())
    totalSinceMonday = db.getTotalDurationSince(getMondayMidnightTimestamp())   

    return render_template('status.html',
            isUpdate=True,
            jstate=state,
            currentPeriode=currentPeriode,
            periodes=allPeriods,
            totalTimestamp=totalDuration,
            totalSinceMonday=totalSinceMonday)

@app.route('/toggle', methods=['POST'])
def toggleWorking():
    db = app.config['db']
    db.toggleWorking()
    return getStatus()


@app.route('/getPeriodes', methods=['GET'])
def getPeriodes():
    db = app.config['db']
    periodes = db.getAllPeriodes()
    return render_template('periodes.html', periodes=periodes)


@app.route('/getDayTotal', methods=['GET'])
def getDayTotal():
    db = app.config['db']

    date = datetime.now()
    date = date.replace(hour=0, minute=0, second=0)
    startOfDayTimestamp = int(date.timestamp())

    totalDuration = db.getTotalDurationSince(startOfDayTimestamp)

    return render_template('dayTotal.html',
        totalTimestamp=totalDuration,
        currentPeriode=db.currentPeriode,)


@app.route("/stream")
def events():
    db = app.config['db']
    
    def SSE():
        yield "event: init\ndata: init\n\n"
        while True:
            status = db.waitChangedFlag()
            yield f"event: newdata\ndata: newdatadata {status}\n\n"
            print("\nsse newdata sent")
    return Response(SSE(), mimetype="text/event-stream")

@app.route("/dropDb",methods=['DELETE'])
def dropDb():
    db = app.config['db']
    db.dropDb()
    db._createDb()
    return "ok"



def webserver(db):
    app.config['db'] = db
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == '__main__':
    print("test webserver")
    from DbAccess import DbAccess
    db = DbAccess()
    webserver(db)
