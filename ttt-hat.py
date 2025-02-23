import sys
import random
import time
from sense_hat import SenseHat


NONE = 0
x_player = 1
o_player = 2
player_symbols = [ ' ', 'X', 'O' ]
board = []
width = 3
height = 3
squares = width * height;

D = [0, 0, 0]       # background
R = [200, 0, 0]     # player mark
Y = [200, 200, 0]   # cursor (clear)
G = [0, 200, 0]     # board lines
B = [0, 0, 200]     # AI player
P = [200, 0, 200]   # cursor (occupied)


board_pixels = [
D, D, G, D, D, G, D, D,
D, D, G, D, D, G, D, D,
G, G, G, G, G, G, G, G,
D, D, G, D, D, G, D, D,
D, D, G, D, D, G, D, D,
G, G, G, G, G, G, G, G,
D, D, G, D, D, G, D, D,
D, D, G, D, D, G, D, D
]
sense = SenseHat()


# Draw the game on the screen
# Include any marks from players so far.
def draw_board():
   sense.set_pixels(board_pixels)


# Take our internal board of X and O and
# convert it into a grid of 8x8 pixels)
def convert_board(my_board):
   board_index = 0
   pixel_index = 0

   for row in range(height):
        for colmn in range(width):
           symbol = my_board[board_index]
           if symbol == 'X':
               colour = R
           elif symbol == 'O':
               colour = B
           else:
               colour = D

           board_pixels[pixel_index] = colour
           board_pixels[pixel_index + 1] = colour
           board_pixels[pixel_index + 8] = colour
           board_pixels[pixel_index + 9] = colour
           board_index += 1
           pixel_index += 3

        pixel_index += 15 


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
   draw_board()

   # pick colour
   offset = (joy_y - 1) * 3
   offset += (joy_x - 1)
   symbol = my_board[offset] 
   if symbol == player_symbols[NONE]:
      colour = Y
   else:
      colour = P

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
          if my_board[target_square] == player_symbols[NONE]:
              finished = True

       draw_board_with_joystick(my_board, joy_x, joy_y)
 
   return target_square


# This function picks the first empty square on a board from
# the provided list. The returned value is the value of the square
# in the range of 0 to 8.
# It should not be possible for a match not to be found, but
# if that is the case then -1 is returned.
def pick_grid_value(my_board, all_options):
    index = 0
    while index < len(all_options):
        target = all_options[index]
        if my_board[target] == player_symbols[NONE]:
           return target
        else:
           index += 1
    return -1

# Try to figure out where the computer controlled player should
# move. The target square needs to be empty.
# We return a square value in the range of 0 to 8.
def get_ai_move(my_board):
   all_possible_moves = []

   # First look to see if we can win the game with this move.
   # We know our player's value is "O" on the board, so
   # we will assign it a value of 7 and the other player's "X"
   # will be assigned a value of 1. Any of the eight lines
   # on the board adding up to exactly 4 means we should take
   # the empty square.
  
   # First check horizontal rows
   start = 0
   while start < squares:
      total = 0
      if my_board[start] == player_symbols[o_player]:
          total += 7
      elif my_board[start] == player_symbols[x_player]:
          total += 1
      if my_board[start + 1] == player_symbols[o_player]:
          total += 7
      elif my_board[start + 1] == player_symbols[x_player]:
          total += 1
      if my_board[start + 2] == player_symbols[o_player]:
          total += 7
      elif my_board[start + 2] == player_symbols[x_player]:
          total += 1
      if total == 14:
         all_possible_moves.append(start) 
         all_possible_moves.append(start + 1) 
         all_possible_moves.append(start + 2) 
         target_square = pick_grid_value(my_board, all_possible_moves)
         return target_square
      else:
         start += 3

   # Next check vertical options for a win
   start = 0
   while start < width:
      total = 0
      if my_board[start] == player_symbols[o_player]:
         total += 7
      elif my_board[start] == player_symbols[x_player]:
         total += 1
      if my_board[start + 3] == player_symbols[o_player]:
         total += 7
      elif my_board[start + 3] == player_symbols[x_player]:
         total += 1
      if my_board[start + 6] == player_symbols[o_player]:
         total += 7
      elif my_board[start + 6] == player_symbols[x_player]:
         total += 1
      if total == 14:
          all_possible_moves.append(start)
          all_possible_moves.append(start + 3)
          all_possible_moves.append(start + 6)
          target_square = pick_grid_value(my_board, all_possible_moves)
          return target_square
      else:
          start += 1

   # Third option, look for win on the diagionals.
   total = 0
   if my_board[0] == player_symbols[o_player]:
      total += 7
   elif my_board[0] == player_symbols[x_player]: 
      total += 1
   if my_board[4] == player_symbols[o_player]:
      total += 7
   elif my_board[4] == player_symbols[x_player]: 
      total += 1
   if my_board[8] == player_symbols[o_player]:
      total += 7
   elif my_board[8] == player_symbols[x_player]: 
      total += 1
   if total == 14:
       all_possible_moves.append(0)
       all_possible_moves.append(4)
       all_possible_moves.append(8)
       target_square = pick_grid_value(my_board, all_possible_moves)
       return target_square

   total = 0
   if my_board[2] == player_symbols[o_player]:
      total += 7
   elif my_board[2] == player_symbols[x_player]:
      total += 1
   if my_board[4] == player_symbols[o_player]:
      total += 7
   elif my_board[4] == player_symbols[x_player]:
      total += 1
   if my_board[6] == player_symbols[o_player]:
      total += 7
   elif my_board[6] == player_symbols[x_player]:
      total += 1
   if total == 14:
       all_possible_moves.append(2)
       all_possible_moves.append(4) 
       all_possible_moves.append(6)
       target_square = pick_grid_value(my_board, all_possible_moves)
       return target_square

   # At this point we cannot win. Maybe we should block?
   # Now we reverse our logic. Squares with an "X" will
   # be worth 7 and any O will be worth 1. When we find
   # any line with a total value of 14 that means the opponent
   # has two of three marks in the line. We should try to
   # block in the final square.

   # Check for block horizontally.
   start = 0
   while start < squares:
      total = 0
      if my_board[start] == player_symbols[x_player]:
          total += 7
      elif my_board[start] == player_symbols[o_player]:
          total += 1
      if my_board[start + 1] == player_symbols[x_player]:
          total += 7
      elif my_board[start + 1] == player_symbols[o_player]:
          total += 1
      if my_board[start + 2] == player_symbols[x_player]:
          total += 7
      elif my_board[start + 2] == player_symbols[o_player]:
          total += 1
      if total == 14:
         all_possible_moves.append(start)
         all_possible_moves.append(start + 1)
         all_possible_moves.append(start + 2)
         target_square = pick_grid_value(my_board, all_possible_moves)
         return target_square
      else:
         start += 3


   # Next check vertical options for a block
   start = 0
   while start < width:
      total = 0
      if my_board[start] == player_symbols[x_player]:
         total += 7
      elif my_board[start] == player_symbols[o_player]:
         total += 1
      if my_board[start + 3] == player_symbols[x_player]:
         total += 7
      elif my_board[start + 3] == player_symbols[o_player]:
         total += 1
      if my_board[start + 6] == player_symbols[x_player]:
         total += 7
      elif my_board[start + 6] == player_symbols[o_player]:
         total += 1
      if total == 14:
          all_possible_moves.append(start)
          all_possible_moves.append(start + 3)
          all_possible_moves.append(start + 6)
          target_square = pick_grid_value(my_board, all_possible_moves)
          return target_square
      else:
          start += 1

   # Third option, look for a block on the diagionals.
   total = 0
   if my_board[0] == player_symbols[x_player]:
      total += 7
   elif my_board[0] == player_symbols[o_player]:
      total += 1
   if my_board[4] == player_symbols[x_player]:
      total += 7
   elif my_board[4] == player_symbols[o_player]:
      total += 1
   if my_board[8] == player_symbols[x_player]:
      total += 7
   elif my_board[8] == player_symbols[o_player]:
      total += 1
   if total == 14:
       all_possible_moves.append(0)
       all_possible_moves.append(4)
       all_possible_moves.append(8)
       target_square = pick_grid_value(my_board, all_possible_moves)
       return target_square

   total = 0
   if my_board[2] == player_symbols[x_player]:
      total += 7
   elif my_board[2] == player_symbols[o_player]:
      total += 1
   if my_board[4] == player_symbols[x_player]:
      total += 7
   elif my_board[4] == player_symbols[o_player]:
      total += 1
   if my_board[6] == player_symbols[x_player]:
      total += 7
   elif my_board[6] == player_symbols[o_player]:
      total += 1
   if total == 14:
       all_possible_moves.append(2)
       all_possible_moves.append(4)
       all_possible_moves.append(6)
       target_square = pick_grid_value(my_board, all_possible_moves)
       return target_square


   # No impending losses to block, try taking the middle?
   if my_board[4] == player_symbols[NONE]:
      return 4

   # Middle is taken, try the corners?
   if my_board[0] == player_symbols[NONE] or my_board[2] == player_symbols[NONE] or my_board[6] == player_symbols[NONE] or my_board[8] == player_symbols[NONE]:
       all_possible_moves = [0, 2, 6, 8]
       random.shuffle(all_possible_moves)
       target_square = pick_grid_value(my_board, all_possible_moves)
       return target_square


   # Cannot find anything better to do, try selecting a random position.
   all_possible_moves.clear()
   for count in range(squares):
       all_possible_moves.append(count)
   random.shuffle(all_possible_moves)
   target_square = pick_grid_value(my_board, all_possible_moves)

   return target_square 


# Show the board and declare who won
def declare_winner(my_board, my_winner):
   draw_board()
   time.sleep(3)
   sense.show_message(my_winner)



# See if we have the player's symbol in any of
# the eight possible winning arrangements.
# Return True if found or False otherwise.
def check_for_win(my_board, player_number):
   found_winner = False
   my_symbol = player_symbols[player_number]
   
   # Check horizontally for wins
   start = 0
   while start < squares and found_winner == False:
        if my_board[start] == my_symbol and my_board[start + 1] == my_symbol and my_board[start + 2] == my_symbol:
               found_winner = True
        else:
           start += 3
        
   # Check vertically
   start = 0
   while start < width and found_winner == False:
        if my_board[start] == my_symbol and my_board[start + 3] == my_symbol and my_board[start + 6] == my_symbol:
              found_winner = True
        else:
           start += 1

   # Check diagonally
   if my_board[0] == my_symbol and my_board[4] == my_symbol and my_board[8] == my_symbol:
         found_winner = True

   if my_board[2] == my_symbol and my_board[4] == my_symbol and my_board[6] == my_symbol:
         found_winner = True

   return found_winner



def main():
   game_finished = False
   moves = 0
   target_square = 0
   found_win = False
   winner = "Tie Game"

   # Initialize board
   sense.set_rotation(180)
   for square in range(squares):
       board.append(player_symbols[NONE])

   while not game_finished:
      convert_board(board)
      draw_board()
      target_square = get_player_move(board)
      board[target_square] = player_symbols[x_player]
      moves += 1
      found_win = check_for_win(board, x_player)

      if found_win:
         game_finished = True
         winner = "You won!"

      elif moves >= squares:
         game_finished = True

      else:
         convert_board(board)
         draw_board()
         target_square = get_ai_move(board)
         board[target_square] = player_symbols[o_player]
         moves += 1
         found_win = check_for_win(board, o_player)
         if found_win:
            game_finished = True
            winner = "Computer player won!"

   # end of while game is not finished
   convert_board(board)
   declare_winner(board, winner)
   # clean up sense hat
   sense.clear()
   sense.stick.get_events()
   sys.exit()


if __name__ == "__main__":
   main()

