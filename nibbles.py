from sense_hat import SenseHat
import signal
import sys
import time
import random


sense = SenseHat()

BRIGHTNESS = 100
RED = (BRIGHTNESS, 0, 0)
YELLOW = (BRIGHTNESS, BRIGHTNESS, 0)
GREEN = (0, BRIGHTNESS, 0)
BLUE = (0, 0, BRIGHTNESS)
PURPLE = (BRIGHTNESS, 0, BRIGHTNESS)
COLOURS = (RED, YELLOW, GREEN, BLUE, PURPLE)
BLACK = (0, 0, 0)
B = BLACK

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT

REFRESH_DELAY = 1.0


def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


# Update all the pixels on the board
def Draw_Board(my_board):
   sense.set_pixels(my_board)

 

def main():
   snake_position = []
   finished = False
   my_board = [ B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B,
                B, B, B, B, B, B, B, B ]

   sense.clear()
   signal.signal(signal.SIGINT, signal_handler)
    
   # Pick starting position and direction
   x = BOARD_WIDTH / 2
   y = BOARD_HEIGHT / 2
   x_y_pair = (x, y)
   snake_position.append(x_y_pair)
   delta_x = random.randint(-1, 1)
   delta_y = random.randint(-1, 1)
   # Do not allow the snake to start motionless
   if delta_x == 0 and delta_y == 0:
      delta_x = 1

   while not finished:
      # add snake to board

      # display board
      Draw_Board(my_board)

      # Check for input to change direction or pause

      # update snake position

      # wait
      time.sleep(REFRESH_DELAY)

   # Game is finished
   sense.clear()


if __name__ == "__main__":
   main()

