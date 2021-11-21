from cellworld_py import *


class Servo_message(Json_object):
    def __init__(self, door_number=0, value=0.0):
        self.door_number = door_number
        self.value = value

