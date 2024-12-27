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


    app.run()

if __name__ == '__main__':
    print("test webserver")
    import threading
    lock = threading.Lock()
    webserver(lock)
