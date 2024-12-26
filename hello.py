import threading
import keyboard

#modules internes
import webserver
import kbdhandle
import DbAccess


if __name__ == '__main__':
    db = DbAccess.DbAccess()

    # kbdthread = threading.Thread(target=kbdhandle, args=(db,))
    webthread = threading.Thread(target=webserver.webserver, args=(db,))
    webthread.start()
    kbdhandle.kbdhandle(db)


