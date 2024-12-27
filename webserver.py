def webserver(db):
    from flask import Flask
    from flask import render_template
    from flask import Response

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        state = db.isActivePeriode
        allPeriods = db.getAllPeriodes()
        currentPeriode = db.currentPeriode

        return render_template('index.html', state=state, currentPeriode=currentPeriode,periodes=allPeriods)

    @app.route('/getStatus', methods=['GET'])
    def getStatus():
        if db.isActivePeriode:
            return f"""<p>Actif depuis: {db.currentPeriode.getStartTimeStr()}</p>"""
        else:
            return """<p>Inactif</p>"""

    @app.route('/toggle', methods=['POST'])
    def toggleWorking():
        db.toggleWorking()
        return getStatus()

    @app.route('/getPeriodes', methods=['GET'])
    def getPeriodes():
        periodes = db.getAllPeriodes()
        output =""
        for periode in periodes:
            output+=f"<li>{periode.getStartTimeStr()} - {periode.getDuration()}</li>"
        return output

    @app.route("/stream")
    def events():
        def SSE():
            while True:
                status = db.getChangedFlag()
                if status:
                    db.resetChangedFlag()
                    yield "event: newdata\ndata: newdata\n\n"
        return Response(SSE(), mimetype="text/event-stream")

    @app.route("/dropDb",methods=['DELETE'])
    def dropDb():
        db.dropDb()
        db._createDb()
        return "ok"

    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == '__main__':
    print("test webserver")
    from DbAccess import DbAccess
    db = DbAccess()
    webserver(db)
