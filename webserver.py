def webserver(dbLock):
    from flask import Flask
    from flask import render_template
    from DbAccess import DbAccess

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        db = DbAccess(dbLock)
        state = db.isActivePeriode
        allPeriods = db.getAllPeriodes()
        currentPeriode = db.currentPeriode

        return render_template('index.html', state=state, currentPeriode=currentPeriode,periodes=allPeriods)

    @app.route('/toggle', methods=['POST'])
    def toggleWorking():
        db = DbAccess(dbLock)
        db.toggleWorking()
        if db.isActivePeriode:
            return f"""<p>Actif depuis: {db.currentPeriode.getStartTimeStr()}</p>"""
        else:
            return """<p>Inactif</p>"""

    @app.route('/getPeriodes', methods=['GET'])
    def getPeriodes():
        db = DbAccess(dbLock)
        periodes = db.getAllPeriodes()
        output =""
        for periode in periodes:
            output+=f"<li>{periode.getStartTimeStr()} - {periode.getDuration()}</li>"
        return output

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    print("test webserver")
    import threading
    lock = threading.Lock()
    webserver(lock)
