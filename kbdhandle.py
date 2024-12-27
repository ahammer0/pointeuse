import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv("ENV") == "opi":
    import time;
    import wiringpi;
    from wiringpi import GPIO;
    wiringpi.wiringPiSetup();
    wiringpi.pinMode(8,GPIO.INPUT);
    wiringpi.pullUpDnControl(8,GPIO.PUD_DOWN);
if os.getenv("ENV") == "dev":
    import keyboard

global interrupt
interrupt = False


def callback():
        global interrupt
        interrupt = True

def seconde():
        global interrupt
        print("itterrupt state",interrupt)
        print("test")
        wiringpi.delay(500)
        interrupt = False



def kbdhandle(db):
    if os.getenv("ENV") == "dev":
        while True:
            print("waiting for key")
            test = input("entre un caractere:(q to quit,t to toggle period)")
            match test:
                case "t":
                    db.toggleWorking()
            print("working state is:",db.isActivePeriode)
    if os.getenv("ENV") == "opi":
        while True:
            if interrupt:
                db.toggleWorking()
                seconde()
