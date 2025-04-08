import threading
import sqlite3
import time
import datetime

import Periode


class DbAccess:
    def __init__(self):
        self.lock = threading.Lock()
        self.con = sqlite3.connect("pointeuse.db", check_same_thread=False)
        self._createDb()

        self.currentPeriode = self._getOpenedPeriode()
        self.isActivePeriode = self.currentPeriode is not None

        self.changedFlag = threading.Event()

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
            self.changedFlag.set()
            self.currantPeriode = None
            self.isActivePeriode = False

    def newPeriode(self):
        with self.lock:
            if not self.isActivePeriode:
                tin = int(time.time())
                cur = self.con.cursor()
                cur.execute(
                    """INSERT INTO periode 
                (timestamp_in) VALUES (?);""",
                    (tin,),
                )
                self.con.commit()

                cur.execute("SELECT * FROM periode WHERE id=?;", (cur.lastrowid,))
                self.currentPeriode = Periode.Periode(cur.fetchone())
                self.isActivePeriode = True
                self.changedFlag.set()

    def _getOpenedPeriode(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""SELECT * FROM periode 
            WHERE timestamp_out IS NULL 
            ORDER BY timestamp_in DESC 
            LIMIT 1;""")
            item = cur.fetchone()
            return Periode.Periode(item) if (item is not None) else None

    def closeLastOpenedPeriode(self):
        with self.lock:
            cur = self.con.cursor()
            cur.execute(
                """UPDATE periode SET timestamp_out = ? 
            WHERE timestamp_out IS NULL 
            ORDER BY timestamp_in DESC 
            LIMIT 1;""",
                (int(time.time()),),
            )
            self.con.commit()

            self.currentPeriode = None
            self.isActivePeriode = False
            self.changedFlag.set()

    def toggleWorking(self):
        if self.isActivePeriode:
            self.closeLastOpenedPeriode()
        else:
            self.newPeriode()

    def getAllPeriodes(self, limitDays=10):
        ts = datetime.datetime.now().timestamp() - limitDays * 24 * 60 * 60
        with self.lock:
            cur = self.con.cursor()
            cur.execute(
                """SELECT * FROM periode WHERE timestamp_out IS NOT NULL AND timestamp_in > ? ORDER BY timestamp_in DESC;""",
                (ts,),
            )
            items = cur.fetchall()
            return [Periode.Periode(item) for item in items]

    def deletePeriode(self, id):
        with self.lock:
            cur = self.con.cursor()
            cur.execute("""DELETE FROM periode where id=?;""", (id,))
            self.con.commit()
            self.changedFlag.set()

    def getTotalDurationSince(self, timestamp):
        with self.lock:
            cur = self.con.cursor()
            cur.execute(
                """SELECT SUM(timestamp_out - timestamp_in) FROM periode WHERE timestamp_in > ?;""",
                (timestamp,),
            )
            data = cur.fetchone()

        if data[0] is None:
            return Periode.Duration(0)
        if self.isActivePeriode:
            return Periode.Duration(
                data[0] + self.currentPeriode.getDuration().toTimestamp()
            )
        else:
            return Periode.Duration(data[0])

    def resetChangedFlag(self):
        with self.lock:
            self.changedFlag.clear()

    def waitChangedFlag(self):
        self.changedFlag.wait()
        self.changedFlag.clear()
        return self.isActivePeriode


if __name__ == "__main__":
    print("test DbAccess")
    db = DbAccess()
    print(db.getAllPeriodes())
    print(db.isActivePeriode, db.currentPeriode)

    print("new periode")
    db.newPeriode()
    db.newPeriode()
    print(db.getAllPeriodes())
    print(db.isActivePeriode, db.currentPeriode)

    time.sleep(1)

    print("toggle working")
    db.toggleWorking()
    print(db.getAllPeriodes())
    print(db.isActivePeriode, db.currentPeriode)

    time.sleep(1)

    print("toggle working")
    db.toggleWorking()
    print(db.getAllPeriodes())
    print(db.isActivePeriode, db.currentPeriode)

    time.sleep(1)

    print("toggle working")
    db.toggleWorking()
    print(db.getAllPeriodes())
    print(db.isActivePeriode, db.currentPeriode)

    print("durée totale")
    print(sum([p.getDuration() for p in db.getAllPeriodes()]))

    db.dropDb()
