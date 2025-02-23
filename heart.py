from sense_hat import SenseHat
import time
import sys
import signal


R = [255,0,0]
B = [0,0,200]

heart = [
B, B, B, B, B, B, B, B,
B, R, R, B, B, R, R, B,
B, R, R, B, B, R, R, B,
B, R, R, R, R, R, R, B,
B, R, R, R, R, R, B, B,
B, B, R, R, R, B, B, B,
B, B, B, R, B, B, B, B,
B, B, B, B, B, B, B, B
]

sense = SenseHat()

def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
sense.set_rotation(180)
sense.set_pixels(heart)
time.sleep(300)
sense.clear(0,0,0)
