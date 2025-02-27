from sense_hat import SenseHat
import signal
import sys
import time

sense = SenseHat()

def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


BRIGHT = 100
HALF_BRIGHT = 50 

RED = (BRIGHT, 0, 0)
ORANGE = (BRIGHT, HALF_BRIGHT, 0)
YELLOW = (BRIGHT, BRIGHT, 0)
GREEN = (0, BRIGHT, 0)
TEAL = (0, BRIGHT, BRIGHT)
BLUE = (0, 0, BRIGHT)
PURPLE = (BRIGHT, 0, BRIGHT)
BLACK = (0, 0, 0)

COLOURS = [ RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE ]
MAX_COLOURS = len(COLOURS)


def main():

    signal.signal(signal.SIGINT, signal_handler)
    sense.clear()
    old_temp = 0
    # start in the middle
    colour_index = round( MAX_COLOURS / 2 ) - 1
    while True:
         temp = sense.get_temperature()
         if old_temp > 0:
            temp_difference = temp - old_temp
            if temp_difference > 0.20:
                colour_index -= 1
                if colour_index < 0:
                   colour_index = 0
                old_temp = temp

            elif temp_difference < -0.20:
                colour_index += 1
                if colour_index >= MAX_COLOURS:
                   colour_index = MAX_COLOURS - 1
                old_temp = temp
         else:
            old_temp = temp

         # end of seeing if temperature changed

         my_colour = COLOURS[colour_index]
         sense.clear(my_colour)
         time.sleep(10)
         # end of while true

if __name__ == "__main__":
    main()

