import os
import signal
import sys
import time
import random


BOARD_WIDTH = 80
BOARD_HEIGHT = 24
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT


def signal_handler(my_signal, temp):
   sys.exit(0)


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
def draw_board(the_board):
   board_index = 0
   my_character = ' '

   os.system("clear")
   for row in range(BOARD_HEIGHT):
       for column in range(BOARD_WIDTH):
           if the_board[board_index]:
              my_character = '*'
           else:
              my_character = ' '
           print(my_character, end='')
           board_index += 1

       print("")



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
   cycle_count = 0

   signal.signal(signal.SIGINT, signal_handler)

   # init board with starting characters
   init_life_board(my_board)
   
   while not finished:
      # display board
      draw_board(my_board)

      # calculate new life positions
      new_board = apply_life_processes(my_board)
      cycle_count += 1

      # See if the board is stuck in a fixed pattern
      # Also reset after five minutes (150 cycles)
      if (new_board == my_board) or (cycle_count > 500):
         init_life_board(my_board)
         cycle_count = 0
      else:
         my_board = new_board

      # wait
      time.sleep(2)



if __name__ == "__main__":
   main()

