def kbdhandle(db):
    while True:
        print("waiting for key")
        test = input("entre un caractere: ")
        db.set(test)

