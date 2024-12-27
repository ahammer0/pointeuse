def kbdhandle(db):
    while True:
        db.newPeriode()
        per = db.getOpenPeriode()
        print(per)
        print("waiting for key")
        test = input("entre un caractere: ")


        db.set(test)

