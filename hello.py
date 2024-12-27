import threading
import keyboard

#modules internes
import webserver
import kbdhandle
import DbAccess


if __name__ == '__main__':
    print("test DbAccess")
    dbLock = threading.Lock()

    webthread = threading.Thread(target=webserver.webserver, args=(dbLock,))
    webthread.start()

    db = DbAccess.DbAccess(dbLock)
    kbdhandle.kbdhandle(db)
