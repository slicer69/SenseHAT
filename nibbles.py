from sense_hat import SenseHat
import math
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
FOOD_COLOUR = GREEN


BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT

REFRESH_DELAY = 1.0

DIR_UP = 0
DIR_DOWN = 2
DIR_LEFT = 1
DIR_RIGHT = 3


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
       board_index = math.trunc( x_y[1] * BOARD_WIDTH + x_y[0] )
       my_board[board_index] = SNAKE_COLOUR
       snake_index += 1


# Find an empty spot where we can put food on the board
# Try at random the first time, then move along the board
# until we find a free spot.
def Place_Food(the_board):
   spot = random.randint(0, BOARD_SIZE - 1)
   # First attempt to find a random spot
   if the_board[spot] == B:
      the_board[spot] = FOOD_COLOUR
   # Random spot was taken, move along the board looking for a new spot
   else:
      spot += 1
      done = False
      while not done:
         # Avoid going off the board
         if spot >= BOARD_SIZE - 1:
            done = True
         else:
            # Found a goo spot, claim it
            if the_board[spot] == B:
               the_board[spot] = FOOD_COLOUR
               done = True
            # This spot is full too, keep looking
            else:
               spot += 1
   
   # Found a good spot, translate the coordinates
   if spot < BOARD_SIZE - 1:
       food_x = spot % BOARD_WIDTH
       food_y = math.trunc(spot / BOARD_WIDTH)
   # Did not find a good spot, return error so we can try again later.
   else:
       food_x = -1
       food_y = -1
   return (food_x, food_y)
 

# Detect if we ran into ourselves or the side of the wall.
# Returns True if we ran unto a wall or ourselves.
# Returns False if we did not run into anything.
def Detect_Collision(the_board, x, y):
    # Check if we are off the board first
    if x < 0 or x > BOARD_WIDTH:
       return True
    if y < 0 or y > BOARD_HEIGHT:
       return True

    # See if we ran into our own colour/tail
    offset = math.trunc( (y * BOARD_WIDTH) + x )
    if the_board[offset] == SNAKE_COLOUR:
        return True
    return False



# Check to see if we wre running into food
def Detect_Food(the_board, x, y):
   offset = math.trunc( (y * BOARD_WIDTH) + x )
   if the_board[offset] == FOOD_COLOUR:
      return True
   return False


# Get an action from the joystick. Waits for the joystick to
# be released before returning the last direction/action
# given.
# When no input is available we return False.
def Joystick_Action():
  # Check for any joystick events
  all_events = sense.stick.get_events()
  while len(all_events) > 0:
      this_event = all_events.pop(0)
      if this_event.action == "released":
          return this_event.direction
          
  return False




# Check for input from joystick.
# Perform validation to make sure the player
# is not trying to reverse course (180 degrees).
# Return the new direction.
def Get_Player_Move(old_direction):
    # In the case of no good input, keep the old direction
    new_direction = old_direction

    direction = Joystick_Action()
    # remember, direction of stick is inverse
    if direction == "up" and old_direction != DIR_UP:
        new_direction = DIR_UP
    elif direction == "down" and old_direction != DIR_DOWN:
        new_direction = DIR_DOWN
    elif direction == "left" and old_direction != DIR_LEFT:
        new_direction = DIR_LEFT
    elif direction == "right" and old_direction != DIR_RIGHT:
        new_direction = DIR_RIGHT
    elif direction == "middle":
        # Pause. Loop until middle button is pressed again.
        pause = True
        while pause:
           direction = Joystick_Action()
           if direction == "middle":
              pause = False
           else:
              time.sleep(REFRESH_DELAY)

    return new_direction


def main():
   snake_position = []
   food_position = (-1, -1)

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
   x = math.trunc( BOARD_WIDTH / 2 )
   y = math.trunc( BOARD_HEIGHT / 2 )
   max_snake_length = 2
   x_y_pair = (x, y)
   snake_position.append(x_y_pair)
   direction = random.randint(0, 3)
   if direction == DIR_UP or direction == DIR_DOWN:
      delta_x = 0
      delta_y = direction - 1
   elif direction == DIR_LEFT or direction == DIR_RIGHT:
      delta_y = 0
      delta_x = direction - 2


   # This is the main game loop
   while not finished:
      # add snake to board
      Place_Snake_On_Board(my_board, snake_position, max_snake_length)

      # Place food on board if required
      if food_position[0] < 0:
         food_position = Place_Food(my_board)

      # display board
      Draw_Board(my_board)

      # Check for input to change direction or pause
      # Make sure we are not turning back on ourselves
      direction = Get_Player_Move(direction)
      if direction == DIR_UP or direction == DIR_DOWN:
          delta_x = 0
          delta_y = direction - 1
      elif direction == DIR_LEFT or direction == DIR_RIGHT:
          delta_y = 0
          delta_x = direction - 2

      # Adjust delta_x and delta_y
      # update snake position, change x and y
      x += delta_x
      y += delta_y
      # Add new position to the head of the snake
      x_y_pair = (x, y)
      snake_position.append(x_y_pair)

      # Detect if we ran into ourselves or a wall
      collision = Detect_Collision(my_board, x, y)
      if collision:
          finished = True
          sense.clear(RED)

      # Detect if we ran into food
      collision = Detect_Food(my_board, x, y)
      if collision:
          max_snake_length += 1
          food_position = (-1, -1)

      # wait
      time.sleep(REFRESH_DELAY)

   # Game is finished
   sense.clear()


if __name__ == "__main__":
   main()

