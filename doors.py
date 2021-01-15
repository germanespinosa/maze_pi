from adafruit_servokit import ServoKit
from time import sleep
from os import path
import json

class Doors:
    def __init__(self):
        self.neutral_values = []
        self.directions = []
        self.opening_time = []
        self.closing_time = []
        self.door_open = []
        self.detected = []

        self.kit = ServoKit(channels=16)
        self.load_calibration()
        for dn in range(4):
            self.door_open.append(False)
            self.no_move(dn)


    def open_door(self, door):
        self.kit.continuous_servo[door].throttle = -.5 * self.directions[door] + self.neutral_values[door]
        sleep(self.opening_time[door])
        self.kit.continuous_servo[door].throttle = self.neutral_values[door]
        sleep(.2)

    def close_door(self, door):
        self.kit.continuous_servo[door].throttle = 0.5 * self.directions[door] + self.neutral_values[door]
        sleep(self.closing_time[door])
        self.kit.continuous_servo[door].throttle = self.neutral_values[door]
        sleep(.2)

    def door_feed (self, door, value):
      self.kit.continuous_servo[door].throttle = 0.1 * self.directions[door] * value + self.neutral_values[door]
      sleep(.2)
      self.kit.continuous_servo[door].throttle = self.neutral_values[door]
      sleep(.2)
      return "fed %f to door %d" % (0.1 * self.directions[door] * value + self.neutral_values[door], door)

    def no_move(self, door):
      global neutral_values
      self.kit.continuous_servo[door].throttle = self.neutral_values[door]
      sleep(.2)

    def calibrate(self, door):
        global neutral_values
        ub = .12
        lb = -.12
        increment = -.005
        value = ub
        self.kit.continuous_servo[door].throttle = value
        if input("opening or closing: (O/c)") == "c":
          direction = 1
        else:
          direction = -1
        while True:
          self.kit.continuous_servo[door].throttle = value
          if input("is it moving: (Y/n)") == "n":
              break
          value += increment
          print(value)
        ub = value
        while True:
          self.kit.continuous_servo[door].throttle = value
          if input("is is still stopped: (Y/n)") == "n":
              break
          value += increment
          print(value)
        lb = value
        calibration = (ub + lb) / 2
        print("the calibration value is :" + str(calibration))
        self.neutral_values[door] = calibration
        self.no_move(door)

    def save_calibration(self):
        for door in range(len(self.neutral_values)):
            f = open("door%d.cal" % door, "w")
            f.write(str(self.neutral_values[door]))
            f.write("\n")
            f.write(str(self.directions[door]))
            f.write("\n")
            f.write(str(self.opening_time[door]))
            f.write("\n")
            f.write(str(self.closing_time[door]))
            f.write("\n")
            f.close()

    def status(self):
        status = []
        for dn in range(4):
            if self.detected[dn]:
                door_status = {}
                door_status["door_number"] = dn
                door_status["state"] = "open" if self.door_open[dn] else "closed"
                door_status["opening_time"] = self.opening_time[dn]
                door_status["closing_time"] = self.closing_time[dn]
                door_status["direction"] = "regular" if self.directions[dn] == 1 else "inverted"
                status.append(door_status)
        return status

    def load_calibration(self):
        for dn in range(4):
            cal_file_name = "door%d.cal" % dn
            if path.exists(cal_file_name):
                lines = open(cal_file_name, "r").readlines()
                self.neutral_values.append(float(lines[0].replace("\n", "")))
                self.directions.append(int(lines[1].replace("\n", "")))
                self.opening_time.append(float(lines[2].replace("\n", "")))
                self.closing_time.append(float(lines[3].replace("\n", "")))
                self.detected.append(True)
            else:
                self.neutral_values.append(0)
                self.directions.append(0)
                self.opening_time.append(0)
                self.closing_time.append(0)
                self.detected.append(False)


