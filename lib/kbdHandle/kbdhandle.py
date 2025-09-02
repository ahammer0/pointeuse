import os
from dotenv import load_dotenv
load_dotenv()

global interrupt
interrupt = False
def callback():
        global interrupt
        interrupt = True

if os.getenv("ENV") == "opi":
    import time;
    import wiringpi;
    from wiringpi import GPIO;
    wiringpi.wiringPiSetup();
    wiringpi.pinMode(8,GPIO.INPUT);
    wiringpi.pullUpDnControl(8,GPIO.PUD_DOWN);
    wiringpi.wiringPiISR(8, GPIO.INT_EDGE_FALLING, callback)
if os.getenv("ENV") == "dev":
    import keyboard

def seconde():
        global interrupt
        print("itterrupt state",interrupt)
        print("test")
        wiringpi.delay(200)
        interrupt = False

def setRedLedOn():
    if os.getenv("ENV") == "opi":
        os.system("echo default-on > /sys/devices/platform/leds/leds/red:status/trigger")
    else:
        print("led is on")

def setRedLedOff():
    if os.getenv("ENV") == "opi":
        os.system("echo none > /sys/devices/platform/leds/leds/red:status/trigger")
    else:
        print("led is on")


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
        statusBuffer = None
        while True:
            status = db.isActivePeriode
            if status != statusBuffer:
                statusBuffer = status
                if status:
                    setRedLedOn()
                else:
                    setRedLedOff()

            if interrupt:
                db.toggleWorking()
                seconde()
