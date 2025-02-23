from sense_hat import SenseHat
import time
import sys
import signal
import random

MIN_BRIGHT = 50
MAX_BRIGHT = 125
DELAY = 0.25

sense = SenseHat()

def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


def main():
   signal.signal(signal.SIGINT, signal_handler)
   sense.clear()

   while True:
      x = random.randint(0, 7)
      y = random.randint(0, 7)
      red = random.randint(MIN_BRIGHT, MAX_BRIGHT)
      green = random.randint(MIN_BRIGHT, MAX_BRIGHT)
      blue = random.randint(MIN_BRIGHT, MAX_BRIGHT)
      sense.set_pixel(x, y, red, green, blue)
      time.sleep(DELAY)
   

if __name__ == "__main__":
   main()

