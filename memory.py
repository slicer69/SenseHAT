import sys
import random
import signal
import time
from sense_hat import SenseHat


width = 3
height = 3
squares = width * height;

DIM_LIGHT = 50
NORMAL_LIGHT = 100
BRIGHT_LIGHT = 200

BLACK = [0, 0, 0]       # background
RED = [NORMAL_LIGHT, 0, 0]     
ORANGE = [NORMAL_LIGHT, DIM_LIGHT, 0]
YELLOW = [NORMAL_LIGHT, NORMAL_LIGHT, 0]   
GREEN = [0, NORMAL_LIGHT, 0]  
TEAL = [0, NORMAL_LIGHT, NORMAL_LIGHT]
BLUE = [0, 0, NORMAL_LIGHT]     
PURPLE = [NORMAL_LIGHT, 0, NORMAL_LIGHT]  
PINK = [NORMAL_LIGHT, DIM_LIGHT, NORMAL_LIGHT]
WHITE = [NORMAL_LIGHT, NORMAL_LIGHT, NORMAL_LIGHT ]

COLOURS = [ RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, PINK ]

BRIGHT_RED = [BRIGHT_LIGHT, 0, 0]
BRIGHT_ORANGE = [BRIGHT_LIGHT, NORMAL_LIGHT, 0]
BRIGHT_YELLOW = [BRIGHT_LIGHT, BRIGHT_LIGHT, 0]
BRIGHT_GREEN = [0, BRIGHT_LIGHT, 0]
BRIGHT_TEAL = [0, BRIGHT_LIGHT, BRIGHT_LIGHT]
BRIGHT_BLUE = [0, 0, BRIGHT_LIGHT]
BRIGHT_PURPLE = [BRIGHT_LIGHT, 0, BRIGHT_LIGHT]
BRIGHT_PINK = [BRIGHT_LIGHT, NORMAL_LIGHT, BRIGHT_LIGHT]

BRIGHT_COLOURS = [ BRIGHT_RED, BRIGHT_ORANGE, BRIGHT_YELLOW,
                   BRIGHT_GREEN, BRIGHT_TEAL, BRIGHT_BLUE,
                   BRIGHT_PURPLE, BRIGHT_PINK ]
                  
D = BLACK
R = RED
O = ORANGE
Y = YELLOW
G = GREEN
T = TEAL
B = BLUE
P = PURPLE
PP = PINK
W = WHITE

board_pixels = [
R, R, W, O, O, W, Y, Y,
R, R, W, O, O, W, Y, Y,
W, W, W, W, W, W, W, W,
G, G, W, D, D, W, T, T,
G, G, W, D, D, W, T, T,
W, W, W, W, W, W, W, W,
B, B, W, P, P, W, PP, PP,
B, B, W, P, P, W, PP,PP 
]
sense = SenseHat()


def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


# Draw the game on the screen
# Include any marks from players so far.
def draw_board(my_board):
   sense.set_pixels(my_board)


# Get an action from the joystick. Waits for the joystick to
# be released before returning the last direction/action
# given.
def joystick_action():
  event = sense.stick.wait_for_event(emptybuffer=True)
  while event.action != "released":
     time.sleep(0.1)
     event = sense.stick.wait_for_event(emptybuffer=True)
  
  sense.stick.get_events()
  return event.direction


# Draw the board, then add the joystick cursor on top.
def draw_board_with_joystick(my_board, joy_x, joy_y):
   # Show the original board, without the cursor
   draw_board(my_board)

   # pick colour
   offset = (joy_y - 1) * 3
   offset += (joy_x - 1)

   # Translate 3x3 grid to 8x8 grid
   x = (joy_x - 1) * 3
   y = (joy_y - 1) * 3

   sense.set_pixel(x, y, colour)
   sense.set_pixel(x + 1, y, colour)
   sense.set_pixel(x, y + 1, colour)
   sense.set_pixel(x + 1, y + 1, colour)


# Get the human player's move. Make sure it does not
# overlap with another mark on the board.
# Return the position of the move in the range of 0-8.
def get_player_move(my_board):
   finished = False
   joy_x = 2
   joy_y = 2

   while not finished:
       draw_board_with_joystick(my_board, joy_x, joy_y)
       direction = joystick_action()
       # move cursor
       # remember, direction of stick is inverse
       if direction == "up" and joy_y < 3:
          joy_y += 1
       elif direction == "down" and joy_y > 1:
          joy_y -= 1
       elif direction == "left" and joy_x < 3:
          joy_x += 1
       elif direction == "right" and joy_x > 1:
          joy_x -= 1
       elif direction == "middle":
          target_square = (joy_y - 1) * 3  + (joy_x - 1)
          finished = True

       draw_board_with_joystick(my_board, joy_x, joy_y)
 
   return target_square





def main():
   game_finished = False
   moves = 0
   prepared_moves = []
   player_correct = True

   signal.signal(signal.SIGINT, signal_handler)
   # Initialize board
   sense.set_rotation(180)
 
   while not game_finished:
      draw_board(board_pixels)
      # Make up new move
      moves += 1

      # Show new series of moves

      # Now test the player
         # Get player move
         # Compare player move to expected move


      # end of while game loop

   # clean up sense hat
   sense.clear()
   sense.stick.get_events()
   sys.exit()


if __name__ == "__main__":
   main()

