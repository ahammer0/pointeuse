import threading
import sqlite3
import time

import Periode

class DbAccess():
    def __init__(self):
        self.lock = threading.Lock()
        self.con = sqlite3.connect('pointeuse.db')
        self._createDb()

        self.currentPeriode = self._getOpenedPeriode()
        self.isActivePeriode = self.currentPeriode is not None

    def _createDb(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS periode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_in NOT NULL,
                timestamp_out NULL);
            """)

    def dropDb(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""DROP TABLE IF EXISTS periode;""")

    def newPeriode(self):
        with self.lock:
            if not self.isActivePeriode:
                tin = int(time.time())
                cur = self.con.cursor()
                cur.execute("""INSERT INTO periode 
                (timestamp_in) VALUES (?);""", (tin,))
                self.con.commit()

                cur.execute("SELECT * FROM periode WHERE id=?;",(cur.lastrowid,))
                self.currentPeriode = Periode.Periode(cur.fetchone())
                self.isActivePeriode = True

    def _getOpenedPeriode(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""SELECT * FROM periode 
            WHERE timestamp_out IS NULL 
            ORDER BY timestamp_in DESC 
            LIMIT 1;""")
            item = cur.fetchone()
            return Periode.Periode(item) if (item is not None)  else None

    def closeLastOpenedPeriode(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""UPDATE periode SET timestamp_out = ? 
            WHERE timestamp_out IS NULL 
            ORDER BY timestamp_in DESC 
            LIMIT 1;""", (int(time.time()),))
            self.con.commit()

            self.currentPeriode = None
            self.isActivePeriode = False

    def toggleWorking(self):
        if self.isActivePeriode:
            self.closeLastOpenedPeriode()
        else:
            self.newPeriode()

    def getAllPeriodes(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""SELECT * FROM periode;""")
            items = cur.fetchall()
            return [Periode.Periode(item) for item in items]

    def deletePeriode(self,id):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""DELETE FROM periode where id=?;""",(id,))
            self.con.commit()


if __name__=="__main__":
    db = DbAccess()
    print(db.getAllPeriodes())
    db.newPeriode()
    db.newPeriode()
    print(db.getAllPeriodes())
    time.sleep(1)
    db.closeLastOpenedPeriode()
    print(db.getAllPeriodes())

    db.dropDb()
