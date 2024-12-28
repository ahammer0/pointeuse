from flask import Flask
from flask import render_template
from flask import Response
from DbAccess import DbAccess
db = DbAccess()

app = Flask(__name__)
app.config['db'] = db

@app.route('/')
def hello_world():
    db = app.config['db']
    state = db.isActivePeriode
    allPeriods = db.getAllPeriodes()
    currentPeriode = db.currentPeriode

    return render_template('index.html', state=state, currentPeriode=currentPeriode,periodes=allPeriods)

@app.route('/getStatus', methods=['GET'])
def getStatus():
    db = app.config['db']
    return render_template('status.html', currentPeriode=db.currentPeriode)

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

@app.route("/stream")
def events():
    db = app.config['db']
    def SSE():
        while True:
            status = db.getChangedFlag()
            if status:
                db.resetChangedFlag()
                yield "event: newdata\ndata: newdata\n\n"
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
