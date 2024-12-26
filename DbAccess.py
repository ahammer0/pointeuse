import threading
import sqlite3
import time

class DbAccess():
    def __init__(self):
        self.lock = threading.Lock()
        self.state=""
        self.con = sqlite3.connect('pointeuse.db')
        self.createDb()

    def createDb(self):
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS periode (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_in NOT NULL,
            timestamp_out NULL);
        """)

    def newPeriode(self):
        tin = time.time()
        cur = self.con.cursor()
        cur.execute("""INSERT INTO periode 
        (timestamp_in) VALUES (?);""", (tin,))

        self.con.commit()

    def getOpenPeriode(self):
        cur = self.con.cursor()
        cur.execute("""SELECT * FROM periode 
        WHERE timestamp_out IS NULL 
        ORDER BY timestamp_in DESC 
        LIMIT 1;""")
        return cur.fetchone()

    def closePeriode(self):
        cur = self.con.cursor()
        cur.execute("""UPDATE periode SET timestamp_out = ? 
        WHERE timestamp_out IS NULL 
        ORDER BY timestamp_in DESC 
        LIMIT 1;""", (time.time(),))
        self.con.commit()

    def get(self):
        with self.lock:
            return self.state

    def set(self, value):
        with self.lock:
            self.state = value
