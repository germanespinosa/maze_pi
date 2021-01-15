
from gpiozero import Button, LED
from time import sleep

feeder = LED(27)

#while True:
#    if not button.is_pressed:
#        print ("feeding")
#        feeder.on()
#        sleep(1)
#        feeder.off()
#        print("not feeding")
 #okays

# for i in range(100):
#     print(i)
#     feeder.on()
#     sleep(.025)
#     feeder.off()
#     sleep(.5)

# for i in range(100):
#     print(i)
#     feeder.on()
#     sleep(10)
#     feeder.off()
#     sleep(1)

for i in range(100):
    print(i)
    feeder.on()
    sleep(.015)
    feeder.off()
    sleep(5)
