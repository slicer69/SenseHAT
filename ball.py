import random
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
DELAY = 0.6

sense = SenseHat()


# Catch signal to quit
def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


def main():
    # Catch Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    x = random.randint(0, MAX_WIDTH - 1)
    y = random.randint(0, MAX_HEIGHT - 1)
    delta_x = 1
    delta_y = 1
    colour_index = 0
    current_colour = COLOURS[colour_index]
    sense.clear()
    while True:
       sense.set_pixel(x, y, current_colour)
       time.sleep(DELAY)
       # Change position
       sense.set_pixel(x, y, BLACK)
       x += delta_x
       y += delta_y
       # Keep position in bounds
       changed_direction = False
       if x < 0:
            x = 1
            delta_x = random.randint(1, 2)
            changed_direction = True
       elif x > MAX_WIDTH - 1:
            x = MAX_WIDTH - 2
            delta_x = random.randint(-2, -1)
            changed_direction = True
       if y < 0:
            y = 1
            delta_y = random.randint(1, 2)
            changed_direction = True
       elif y > MAX_HEIGHT - 1:
            y = MAX_HEIGHT - 2
            delta_y = random.randint(-2, -1)
            changed_direction = True
        
       if changed_direction:
          colour_index += 1
          if colour_index >= MAX_COLOURS:
             colour_index = 0
          current_colour = COLOURS[colour_index]


if __name__ == "__main__":
   main()

