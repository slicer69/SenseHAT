from sense_hat import SenseHat
import math
import time
import sys
import signal


SLEEP_DELAY = 1

BRIGHTNESS = 150
RED = [BRIGHTNESS,0,0]
GREEN = [0,BRIGHTNESS,0]
BLUE = [0,0,BRIGHTNESS]
BLACK = [0,0,0]
B = BLACK

canvas = [
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
]

CANVAS_WIDTH = 8
CANVAS_HEIGHT = 8
NUMBER_HEIGHT = 4
NUMBER_WIDTH = 4
NUMBER_SIZE = NUMBER_HEIGHT * NUMBER_WIDTH

numbers = [
0,1,1,1, # Zero
0,1,0,1,
0,1,0,1,
0,1,1,1,
0,0,1,0, # One
0,1,1,0,
0,0,1,0,
0,1,1,1,
0,1,1,1, # Two
0,0,1,1,
0,1,1,0,
0,1,1,1,
0,1,1,1, # Three
0,0,1,1,
0,0,1,1,
0,1,1,1,
0,1,0,1, # Four
0,1,1,1,
0,0,0,1,
0,0,0,1,
0,1,1,1, # Five
0,1,1,0,
0,0,1,1,
0,1,1,1,
0,1,0,0, # Six
0,1,1,1,
0,1,0,1,
0,1,1,1,
0,1,1,1, # Seven
0,0,0,1,
0,0,1,0,
0,1,0,0,
0,1,1,1, # Eight
0,1,1,1,
0,1,1,1,
0,1,1,1,
0,1,1,1, # Nine
0,1,0,1,
0,1,1,1,
0,0,0,1
]

sense = SenseHat()

def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)


def Clear_Canvas():
   for index in range(0, CANVAS_WIDTH * CANVAS_HEIGHT):
      canvas[index] = BLACK


def Place_Number_On_Canvas(x, y, value, colour):
   if value > 9:
       tens = math.trunc(value / 10)
       ones = value % 10
   else:
       tens = 0
       ones = value

   canvas_index = y * CANVAS_WIDTH + x
   number_index = tens * NUMBER_SIZE
   for line in range(0, NUMBER_HEIGHT):
     for column in range(0, NUMBER_WIDTH):
         if numbers[number_index] == 1:
            canvas[canvas_index] = colour
         else:
            canvas[canvas_index] = BLACK
         canvas_index += 1
         number_index += 1
     canvas_index = canvas_index + (CANVAS_WIDTH - NUMBER_WIDTH)

   canvas_index = y * CANVAS_WIDTH + x + NUMBER_WIDTH
   number_index = ones * NUMBER_SIZE
   for line in range(0, NUMBER_HEIGHT):
     for column in range(0, NUMBER_WIDTH):
         if numbers[number_index] == 1:
            canvas[canvas_index] = colour
         else:
            canvas[canvas_index] = BLACK
         canvas_index += 1
         number_index += 1
     canvas_index = canvas_index + (CANVAS_WIDTH - NUMBER_WIDTH)


def main():
   signal.signal(signal.SIGINT, signal_handler)
   sense.set_rotation(180)

   while True:
      my_time = time.localtime()
      my_minute = my_time.tm_min
      my_hour = my_time.tm_hour

      Place_Number_On_Canvas(0, 0, my_hour, GREEN)
      Place_Number_On_Canvas(0, 4, my_minute, RED)
      sense.clear()
      sense.set_pixels(canvas)
      Clear_Canvas()
      time.sleep(SLEEP_DELAY)


if __name__ == "__main__":
    main()

