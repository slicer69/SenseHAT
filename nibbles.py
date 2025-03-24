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
SNAKE_COLOUR = YELLOW

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


# This function draws the snake on the board.
# The first parameter is the board itself. The
# second parameter is a list of x,y coordinates
# which we will use to place the snake.
# Before we draw the snake we may need to erase the
# end of its tail. If the snakes current length is
# greater than max_snake, then we erase its tail.
# The "head" of the snake is at the end of the list
# and the "tail" is at the beginning of the list. 
def Place_Snake_On_Board(my_board, snake, max_snake):
   # First, erase the tail if needed
   if max_snake > 1:
      while len(snake) > max_snake:
          x_y = snake.pop(0)
          board_index = x_y[1] * BOARD_WIDTH + x_y[0]
          my_board[board_index] = BLACK

   # Now draw the entire remaining snake
   snake_index = 0
   while snake_index < len(snake):
       x_y = snake[snake_index]
       board_index = x_y[1] * BOARD_WIDTH + x_y[0]
       my_board[board_index] = SNAKE_COLOUR




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
   max_snake_length = 2
   x_y_pair = (x, y)
   snake_position.append(x_y_pair)
   delta_x = random.randint(-1, 1)
   delta_y = random.randint(-1, 1)
   # Do not allow the snake to start motionless
   if delta_x == 0 and delta_y == 0:
      delta_x = 1

   while not finished:
      # add snake to board
      Place_Snake_On_Board(my_board, snake_position, max_snake_length)

      # display board
      Draw_Board(my_board)

      # Check for input to change direction or pause
      # Make sure we are not turning back on ourselves
      # Adjust delta_x and delta_y
     
      # update snake position, change x and y
      x += delta_x
      y += delta_y

      # Detect if we ran into ourselves or a wall
      collision = Detect_Collision(my_board, x, y)
      if collision:
          finished = True
          sense.clear(RED)

      # wait
      time.sleep(REFRESH_DELAY)

   # Game is finished
   sense.clear()


if __name__ == "__main__":
   main()

