import math
import sys
import random
import signal
import time
from sense_hat import SenseHat


width = 3
height = 3
squares = width * height;
middle_square = 4
pixels_width = 8
pixels_height = 8

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

COLOURS = [ RED, ORANGE, YELLOW, GREEN, TEAL, PINK, BLUE, PURPLE ]

BRIGHT_RED = [BRIGHT_LIGHT, 0, 0]
BRIGHT_ORANGE = [BRIGHT_LIGHT, NORMAL_LIGHT, 0]
BRIGHT_YELLOW = [BRIGHT_LIGHT, BRIGHT_LIGHT, 0]
BRIGHT_GREEN = [0, BRIGHT_LIGHT, 0]
BRIGHT_TEAL = [0, BRIGHT_LIGHT, BRIGHT_LIGHT]
BRIGHT_BLUE = [0, 0, BRIGHT_LIGHT]
BRIGHT_PURPLE = [BRIGHT_LIGHT, 0, BRIGHT_LIGHT]
BRIGHT_PINK = [BRIGHT_LIGHT, NORMAL_LIGHT, BRIGHT_LIGHT]

BRIGHT_COLOURS = [ BRIGHT_RED, BRIGHT_ORANGE, BRIGHT_YELLOW,
                   BRIGHT_GREEN, BRIGHT_TEAL, BRIGHT_PINK,
                   BRIGHT_BLUE, BRIGHT_PURPLE ]
                  
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
PP, PP, W, B, B, W, P, P,
PP, PP, W, B, B, W, P, P 
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

   # Translate 3x3 grid to 8x8 grid
   x = (joy_x - 1) * 3
   y = (joy_y - 1) * 3
   # Get the colour at x/y, then
   # match it to a bright colour.
   offset = ( (joy_y - 1) * width * pixels_width) + x 
   original_colour = my_board[offset]

   found_colour = False
   colour_index = 0
   while not found_colour and colour_index < len(COLOURS):
      if COLOURS[colour_index] == original_colour:
         found_colour = True
      else:
         colour_index += 1

   if found_colour:
       new_colour = BRIGHT_COLOURS[colour_index]
   else:
       new_colour = WHITE

   sense.set_pixel(x, y, new_colour)
   sense.set_pixel(x + 1, y, new_colour)
   sense.set_pixel(x, y + 1, new_colour)
   sense.set_pixel(x + 1, y + 1, new_colour)


# Get the human player's move.
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
          target_square = (joy_y - 1) * width  + (joy_x - 1)
          # Player cannot select middle square
          if target_square != middle_square:
               finished = True

       draw_board_with_joystick(my_board, joy_x, joy_y)
 
   return target_square


# Flash the appropriate colours on the board.
# Show the appropriate square in bright colour for a second
# then clear the board, then show the next colour.
def Show_Moves(my_board, my_moves):
   move_index = 0

   draw_board(my_board)
   while move_index < len(my_moves):
      colour_index = my_moves[move_index]
      # Light up board with chosen colour
      if colour_index >= middle_square:
         target_square = colour_index + 1
      else:
         target_square = colour_index
   
      # Translate square into x/y coordinates
      x = target_square % 3
      y = math.trunc(target_square / width)
      x *= 3
      y *= 3

      bright_colour = BRIGHT_COLOURS[colour_index]
      sense.set_pixel(x, y, bright_colour)
      sense.set_pixel(x + 1, y, bright_colour)
      sense.set_pixel(x, y + 1, bright_colour)
      sense.set_pixel(x + 1, y + 1, bright_colour)

      time.sleep(1)
      draw_board(my_board)
      time.sleep(1)
      move_index += 1


# This function gets a player's move, using the joystick
# then compares it against the known good moves provided.
# If the player gets all matching moves correct, the function
# returns True. If a mistake is made, the function returns
# False.
def Get_Player_Moves(my_board, the_moves):
    move_index = 0
    finished = False
    correct = True

    # Go through all moves until we reach the end or
    # the player gets a match wrong.
    while not finished and correct:
        correct_move = the_moves[move_index]
        player_move = get_player_move(my_board)
        # Compensate for blank middle square
        if player_move >= middle_square:
           player_move -= 1

        if player_move == correct_move:
           move_index += 1
           if move_index >= len(the_moves):
              finished = True
        else:
           correct = False

    return correct


def Show_Success(my_board):
    draw_board(my_board)
    sense.set_pixel(3, 3, BRIGHT_GREEN)
    sense.set_pixel(4, 3, BRIGHT_GREEN)
    sense.set_pixel(3, 4, BRIGHT_GREEN)
    sense.set_pixel(4, 4, BRIGHT_GREEN)
    time.sleep(2)



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
      time.sleep(2)

      # Make up new move
      colour_index = random.randint( 0, len(COLOURS) - 1 )
      prepared_moves.append(colour_index)

      # Show new series of moves
      Show_Moves(board_pixels, prepared_moves)

      # Now test the player
      status = Get_Player_Moves(board_pixels, prepared_moves)
      if status:
          moves += 1
          Show_Success(board_pixels)
      else:
          game_finished = True
          sense.clear()
          sense.show_message("You completed ")
          sense.show_message( str(moves) )
          sense.show_message(" rounds.")

      # end of while game loop

   # clean up sense hat
   sense.clear()
   sense.stick.get_events()
   sys.exit()


if __name__ == "__main__":
   main()

