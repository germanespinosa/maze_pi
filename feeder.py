import os
from gpiozero import Button, LED
from time import sleep
import requests 
from _thread import start_new_thread
from os import path

def feeder_process(feeder):
    feeder.active = False
    while True: #loops forever
        print ("feeder not enabled")
        while not feeder.active:
            pass
        print ("feeder enabled")
        feeder.active = False
        while True: #wait until the mouse touches the feeder
            if not feeder.sensor.is_pressed:
                feeder.feed()
                feeder.report_feeder()
                break

class Feeder:
    def __init__(self, feed_time, feeder_number):
        self.feeding_time = feed_time #60ms
        self.sensor = Button(17)
        self.number = feeder_number
        self.solenoid = LED(27)
        self.active = False
        if not self.sensor.is_pressed:
            self.sensor = Button(22)
            self.number = 2

    def status(self):
        return {"feeder_number": self.number, "state": "enabled" if self.active else "disabled", "feeding_time": self.feeding_time}

    def test(self, feed_time, reps, wait_time):
        for i in range(reps):
            self.feed(feed_time)
            sleep(wait_time)

    def save_calibration(self, feed_time):
        self.feeding_time = feed_time
        with open("feeder.cal", "w") as f:
            f.write(str(self.feeding_time) + "\n")
            f.write(str(self.number) + "\n")

    def report_feeder(self):
      uri = "http://192.168.137.1"
      uri += ":8081/feeder/" + str(self.number)
      response = requests.get(uri)

    def feed(self, feeding_time=None):
        if feeding_time is None:
            feeding_time = self.feeding_time
        self.solenoid.on()
        sleep(feeding_time)
        self.solenoid.off()


feed_time = 0
feeder_number = 0
if path.exists("feeder.cal"):
    with open("feeder.cal", "r") as f:
        lines = f.readlines()
        feed_time = float(lines[0].replace("\n", ""))
        feeder_number = int(lines[1].replace("\n", ""))

singleton = Feeder(feed_time,feeder_number)
singleton_thread = start_new_thread(feeder_process, (singleton,))

