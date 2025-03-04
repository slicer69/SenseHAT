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

REST_TIME = 0.15


# Take the current colour and advance each of its RGB
# elements one step closer to the target colour's.
# Return the new colour that is a step closer to target.
def Advance_Colour(current_colour, target_colour):
   colours = [0, 0, 0]

   for rgb in range( len(target_colour) ):
      if current_colour[rgb] < target_colour[rgb]:
         colours[rgb] = current_colour[rgb] + 1
      elif current_colour[rgb] > target_colour[rgb]:
         colours[rgb] = current_colour[rgb] - 1
      else:
         colours[rgb] = current_colour[rgb]

   temp_colour = (colours[0], colours[1], colours[2])
   return temp_colour


def main():

    signal.signal(signal.SIGINT, signal_handler)
    sense.clear()

    sense.colour.integration_cycles = 50
    sense.colour.gain = 1

    # start in the middle
    colour_index = round( MAX_COLOURS / 2 ) - 1
    my_colour = COLOURS[colour_index]
    colour_index += 1
    next_colour = COLOURS[colour_index]

    # Check current light levels
    background_light = sense.colour.clear

    while True:

         # Cycle through to next colour
         my_colour = Advance_Colour(my_colour, next_colour)
         # Show the current colour in the dark or turn off the
         # screen in the light
         if background_light < 100:
             sense.clear(my_colour)
         else:
             sense.clear()

         if my_colour == next_colour:
            colour_index += 1
            if colour_index >= MAX_COLOURS:
               colour_index = 0
            next_colour = COLOURS[colour_index]
            # Refresh light level
            background_light = sense.colour.clear

         time.sleep(REST_TIME)
         # end of while true

if __name__ == "__main__":
    main()

