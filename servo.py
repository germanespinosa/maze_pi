from adafruit_servokit import ServoKit
from gpiozero import Button, LED
from time import sleep


kit = ServoKit(channels=16)

button = Button (17)
feeder = LED(27)

while True:
    if not button.is_pressed:
        print ("feeding")
        feeder.on()
        kit.continuous_servo[0].throttle = 1
        kit.continuous_servo[1].throttle = 1
        sleep(2)
        kit.continuous_servo[0].throttle = -1
        kit.continuous_servo[1].throttle = -1
        sleep(2)
        kit.continuous_servo[0].throttle = 0
        kit.continuous_servo[1].throttle = 0
        feeder.off()
        print ("not feeding")
