import math
import signal
import sys
import time
from sense_hat import SenseHat

MAX_WIDTH = 8
MAX_HEIGHT = 8
MAX_SQUARES = MAX_WIDTH * MAX_HEIGHT

BRIGHT = 156
HALF_BRIGHT = 78

RED = (BRIGHT, 0, 0)
ORANGE = (BRIGHT, HALF_BRIGHT, 0)
YELLOW = (BRIGHT, BRIGHT, 0)
WHITE = (BRIGHT, BRIGHT, BRIGHT)
GREEN = (0, BRIGHT, 0)
TEAL = (0, BRIGHT, BRIGHT)
BLUE = (0, 0, BRIGHT)
PURPLE = (BRIGHT, 0, BRIGHT)
BLACK = (0, 0, 0)

COLOURS = [ RED, ORANGE, YELLOW, WHITE, GREEN, TEAL, BLUE, PURPLE ]
MAX_COLOURS = len(COLOURS)

sense = SenseHat()
sense.set_rotation(180)


# Catch signal to quit
def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)



def main():
    # Catch Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    # Get time from command line
    if len(sys.argv) < 2:
       print("Please provide the time to wait in seconds.")
       sys.exit(1)

    if not sys.argv[1].isnumeric():
       print("Please specify, as a number, the amount of time to wait.")
       sys.exit(2)

    seconds = round( int(sys.argv[1]) )
    if seconds < 1:
       print("Number of seconds should be one or greater.")
       sys.exit(3)

    lights_per_second = MAX_SQUARES / seconds
    squares_per_colour = round(MAX_SQUARES / len(COLOURS) )

    # initialize board
    min_x = 0
    min_y = 0
    max_x = MAX_WIDTH
    max_y = MAX_HEIGHT
    x = min_x
    y = min_y
    delta_x = 1
    delta_y = 0
    pixel_count = 0
    colour_index = 0
    current_colour = COLOURS[colour_index]
    squares_in_this_colour = 0
    while pixel_count <= MAX_SQUARES:
        sense.set_pixel(x, y, current_colour)
        time.sleep(0.05)
        pixel_count += 1
        squares_in_this_colour += 1
        if squares_in_this_colour >= squares_per_colour:
           if colour_index < MAX_COLOURS - 1:
               colour_index += 1
           current_colour = COLOURS[colour_index]
           squares_in_this_colour = 0

        x = x + delta_x 
        y = y + delta_y
        if x >= max_x:
           x = max_x - 1
           y += 1
           delta_x = 0
           delta_y = 1
        elif y >= max_y:
           y = max_y - 1
           x -= 1
           delta_x = -1
           delta_y = 0
        elif x < min_x:
           x = min_x
           y -= 1
           delta_x = 0
           delta_y = -1
           min_y += 1
        elif y < min_y:
           min_x += 1
           max_x -= 1
           max_y -= 1
           delta_y = 0
           delta_x = 1
           x = min_x
           y = min_y

    # end of initializing

    # run countdown
    min_x = 0
    min_y = 0
    max_x = MAX_WIDTH
    max_y = MAX_HEIGHT
    delta_y = 0
    delta_x = 1
    x = min_x
    y = min_y
    current_colour = BLACK
    seconds_passed = 0
    pixels_to_kill = 0
    killed_pixels = 0
    while seconds_passed < seconds:
       time.sleep(1)
       seconds_passed += 1
       pixels_to_kill += lights_per_second
       if pixels_to_kill >= 1:
           while killed_pixels < math.trunc(pixels_to_kill):
               sense.set_pixel(x, y, BLACK)
               killed_pixels += 1
               x = x + delta_x
               y = y + delta_y

               if x >= max_x:
                  x = max_x - 1
                  y += 1
                  delta_x = 0
                  delta_y = 1
               elif y >= max_y:
                  y = max_y - 1
                  x -= 1
                  delta_x = -1
                  delta_y = 0
               elif x < min_x:
                   x = min_x
                   y -= 1
                   delta_x = 0
                   delta_y = -1
                   min_y += 1
               elif y < min_y:
                   min_x += 1
                   max_x -= 1
                   max_y -= 1
                   delta_y = 0
                   delta_x = 1
                   x = min_x
                   y = min_y

    # finished putting out the lights. Time to clean up
    sense.clear()
    sys.exit(0)


if __name__ == "__main__":
   main()

