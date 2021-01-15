import os
from gpiozero import Button, LED
from time import sleep
import requests 
from _thread import start_new_thread


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
    def __init__(self, feedtime):
        self.feeding_time = feedtime #60ms
        self.sensor = Button (17)
        self.number = 1 
        self.solenoid = LED(27)
        self.active = False
        if not self.sensor.is_pressed:
            self.sensor = Button (22)
            self.number = 2 

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



singleton = Feeder(.015)


singleton_thread = start_new_thread(feeder_process, (singleton,))

