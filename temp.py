from sense_hat import SenseHat
import signal
import sys
import time

sense = SenseHat()

def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)

signal.signal(signal.SIGINT, signal_handler)

sense.set_rotation(180)

while True:
    temp = sense.get_temperature()
    show_temp = round(temp)
    if (show_temp < 30):
       my_colour = blue
    elif (show_temp < 50):
       my_colour = green
    else:
       my_colour = red

    sense.show_message( str(show_temp), text_colour=my_colour)
    time.sleep(10)

