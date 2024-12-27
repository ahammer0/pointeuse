#!/usr/bin/python3
import threading

#modules internes
import webserver
import kbdhandle
import DbAccess


if __name__ == '__main__':
    print("test DbAccess")
    db = DbAccess.DbAccess()

    webthread = threading.Thread(target=webserver.webserver, args=(db,))
    webthread.start()

    kbdhandle.kbdhandle(db)
