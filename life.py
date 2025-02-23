from sense_hat import SenseHat
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

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT


# Place the initial life forms on the board
def init_life_board(the_board):
    the_board.clear()
    for index in range(BOARD_SIZE):
         number = random.randrange(0,4)
         if number == 3:
            the_board.append(True)
         else:
            the_board.append(False)


# Set the LED lights to match the matrix of
# life forms.
def draw_board(the_board, my_colour):
   board_index = 0
   use_colour = BLACK

   for row in range(BOARD_HEIGHT):
       for column in range(BOARD_WIDTH):
           if the_board[board_index]:
              use_colour = my_colour
           else:
              use_colour = BLACK
           sense.set_pixel(column, row, use_colour)
           board_index += 1



# Apply the rules for the game of Life
# using the values (True/False) in old_board
# and constructing a new board to return.
# Rules:
# 1. If a cell is On and has fewer than 2 neighbours, it turns Off.
# 2. If a cell is On and has two or three neighbours, it stays On.
# 3. If a cell is On and has more than three neighbours, it turns Off.
# 4. If a cell is Off and has three enighbours, it turns On.
def apply_life_processes(old_board):
   new_board = []

   board_index = 0
   for row in range(BOARD_HEIGHT):
     for column in range(BOARD_WIDTH):
        cell = old_board[board_index]

        # count all neighbouring cells
        neighbour_count = 0
        # upper-left
        if (row >= 1) and (column >= 1):
           target = board_index - BOARD_WIDTH - 1
           if old_board[target]:
              neighbour_count += 1

        # directly above
        if row >= 1:
           target = board_index - BOARD_WIDTH
           if old_board[target]:
              neighbour_count += 1

        # upper-right
        if (row >= 1) and (column < BOARD_WIDTH - 1):
           target = board_index - BOARD_WIDTH + 1
           if old_board[target]:
              neighbour_count += 1

        # directly left
        if column > 0:
           target = board_index - 1
           if old_board[target]:
              neighbour_count += 1

        # directly right
        if column < BOARD_WIDTH - 1:
           target = board_index + 1
           if old_board[target]:
              neighbour_count += 1

        # lower-left
        if (column > 0) and (row < BOARD_HEIGHT - 1):
           target = board_index + BOARD_WIDTH - 1
           if old_board[target]:
              neighbour_count += 1
 
        # directly below
        if row < BOARD_HEIGHT - 1:
           target = board_index + BOARD_WIDTH
           if old_board[target]:
              neighbour_count += 1

        # lower-right
        if (row < BOARD_HEIGHT - 1) and (column < BOARD_WIDTH - 1):
           target = board_index + BOARD_WIDTH + 1
           if old_board[target]:
              neighbour_count += 1

        # Apply Life rules
        if cell and neighbour_count < 2:
           cell = False
        elif cell and neighbour_count == 2:
           cell = True
        elif cell and neighbour_count == 3:
           cell = True
        elif cell and neighbour_count > 3:
           cell = False
        elif cell == False and neighbour_count == 3:
           cell = True

        new_board.append(cell)
        board_index += 1

   return new_board

 

def main():
   finished = False
   my_board = []
   colour_index = 0
   max_colour = len(COLOURS)
   life_colour = COLOURS[colour_index]
   sense.clear()

   # init board with starting characters
   init_life_board(my_board)
   
   while not finished:
      # display board
      draw_board(my_board, life_colour)

      # calculate new life positions
      new_board = apply_life_processes(my_board)

      # See if the board is stuck in a fixed pattern
      if new_board == my_board:
         init_life_board(my_board)
      else:
         my_board = new_board

      # cycle colours
      colour_index += 1
      if colour_index >= max_colour:
         colour_index = 0
      life_colour = COLOURS[colour_index]

      # wait
      time.sleep(2)

      # check for input
      events = sense.stick.get_events()
      if len(events) > 0:
         finished = True

   sense.clear()


if __name__ == "__main__":
   main()

