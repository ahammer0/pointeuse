def webserver(dbLock):
    from flask import Flask
    import DbAccess

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        db = DbAccess.DbAccess(dbLock)
        state = db.isActivePeriode
        allPeriods = db.getAllPeriodes()

        return f"<p>{state}</p>\n<p>{allPeriods}</p>"

    app.run()

if __name__ == '__main__':
    print("test webserver")
    import threading
    lock = threading.Lock()
    webserver(lock)
