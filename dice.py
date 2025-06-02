from sense_hat import SenseHat
import math
import random
import sys

BRIGHTNESS = 100
BLACK = [0,0,0]
RED = [BRIGHTNESS,0,0]
PURPLE = [BRIGHTNESS,0,BRIGHTNESS]
GREEN = [0,BRIGHTNESS,0]
BLUE = [0,0,BRIGHTNESS]
COLOURS = [RED, PURPLE, GREEN, BLUE]

DEFAULT_DICE_SIDES = 6
DISPLAY_HEIGHT = 8
DISPLAY_WIDTH = 8
DISPLAY_SIZE = DISPLAY_HEIGHT * DISPLAY_WIDTH

def main():
   sense = SenseHat()
   # sense.set_rotation(180)
   sense.clear()

   my_board = []
   max_sides = DEFAULT_DICE_SIDES
   if len(sys.argv) > 1:
      try:
         max_sides = int(sys.argv[1])
      except:
         print("Please pick a whole number in the range of 1 to 20.")
         sys.exit(1)
      if max_sides < 3 or max_sides > 20:
         print("Please pick a number in the range of 1 to 20.")
         sys.exit(1)

   # Select a colour
   colour_index = random.randint(0, len(COLOURS) - 1)
   random_colour = COLOURS[colour_index]

   # pick a number from one to six (or the max sides of dice)
   my_number = random.randint(1, max_sides)
   print(my_number)

   # Clear the board
   for board_index in range(DISPLAY_SIZE):
         my_board.append(BLACK)

   # Work out the spacing
   centre_row = DISPLAY_WIDTH // 2
   centre_col = DISPLAY_HEIGHT // 2
   distance_between_dots = math.floor(math.sqrt(DISPLAY_SIZE / my_number))
   # Place dots
   for dots in range(my_number):
        # Calculate the angle of the current True value
        angle = 2 * math.pi * dots / my_number

        row = centre_row + math.floor(math.cos(angle) * (DISPLAY_HEIGHT - 1) / 2)
        col = centre_col + math.floor(math.sin(angle) * (DISPLAY_WIDTH - 1) / 2)

        # Adjust the row and column to be within the valid range
        row = max(0, min(row, DISPLAY_HEIGHT - 1))
        col = max(0, min(col, DISPLAY_WIDTH - 1))
        board_index = (row * DISPLAY_WIDTH) + col
        my_board[board_index] = random_colour

   sense.set_pixels(my_board)
   input()
   sense.clear()

if __name__ == "__main__":
   main()

