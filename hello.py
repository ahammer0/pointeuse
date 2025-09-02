#!/usr/bin/python3
import threading

# modules internes
import webserver
import lib.kbdhandle
import lib.DbAccess as DbAccess


if __name__ == "__main__":
    db = DbAccess.DbAccess()

    webthread = threading.Thread(target=webserver.webserver, args=(db,))
    webthread.start()

    kbdhandle.kbdhandle(db)
