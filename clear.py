from sense_hat import SenseHat
import time

sense = SenseHat()

sense.clear(200,0,0)
time.sleep(1)
sense.clear(0,0,200)
time.sleep(1)
sense.clear(0,200,0)
time.sleep(1)
sense.clear(0,0,0)
