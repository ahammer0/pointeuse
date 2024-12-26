from flask import Flask
def webserver(db):
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        db = app.config['db']
        nbr = db.get()
        return f"<p>Hello, World!{nbr}</p>"

    app.config['db'] = db
    app.run()
