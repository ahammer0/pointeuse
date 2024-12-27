def kbdhandle(db):
    while True:
        print("waiting for key")
        test = input("entre un caractere:(q to quit,t to toggle period)")
        match test:
            case "t":
                db.toggleWorking()
        print("working state is:",db.isActivePeriode)
