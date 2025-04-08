from sense_hat import SenseHat
import random
import time
import sys
import signal

WIDTH = 8
HEIGHT = 8

BRIGHT = 150
DIM =  70
DARK = 50
RED = [BRIGHT,0,0]
BROWN = [DARK, 0, 0]
YELLOW = [BRIGHT, BRIGHT, 0]
GREEN = [0,BRIGHT,0]
BLUE = [0,0,BRIGHT]
PURPLE = [BRIGHT,0,BRIGHT]
BLACK = [0,0,0]
LIGHT_COLOURS = [RED, YELLOW, BLUE, PURPLE]
B = BLACK
Y = YELLOW
G = GREEN
T = BROWN
RGB = 3
CHANGE_COLOUR = 5

TIME_DELAY = 0.1

tree = [
B, B, B, B, Y, B, B, B,
B, B, B, G, G, B, B, B,
B, B, B, G, G, G, B, B,
B, B, G, G, G, G, B, B,
B, B, G, G, G, G, G, B,
B, G, G, G, G, G, G, B,
B, B, B, T, T, B, B, B,
B, B, B, T, T, B, B, B
]

sense = SenseHat()

class Light:
   def __init__(self, x, y):
      self.x = x
      self.y = y
      self.colour_index = random.randint(0, len(LIGHT_COLOURS) - 1)
      self.colour = [0,0,0]
      self.delta_colour = [0,0,0]
      # Set how much to change RGB values
      for index in range(RGB):
          self.colour[index] = LIGHT_COLOURS[self.colour_index][index]
          # Start all lights at slightly different levels
          if self.colour[index] > DIM:
             random_brightness = random.randint(-20, 40)
             self.colour[index] += random_brightness

          if self.colour[index] == 0:
             self.delta_colour[index] = 0
          else:
             self.delta_colour[index] = -CHANGE_COLOUR

   def Get_X(self):
       return self.x


   def Get_Y(self):
       return self.y

   def Get_Colour(self):
       return self.colour


   def Change_Colour(self):
      # Move to the next colour in the list
      new_colour = random.randint(0, len(LIGHT_COLOURS) - 1)
      while self.colour_index == new_colour:
           new_colour = random.randint(0, len(LIGHT_COLOURS) - 1)
      
      self.colour_index = new_colour
      # Set how much to change RGB values
      for index in range(RGB):
          if LIGHT_COLOURS[self.colour_index][index] == 0:
             self.colour[index] = 0
             self.delta_colour[index] = 0
          else:
             self.colour[index] = DIM
             self.delta_colour[index] = CHANGE_COLOUR
     

   def Brightness_Down(self):
       # Reduce each colour value
       for index in range(RGB):
          self.colour[index] += self.delta_colour[index]
          
          # When we hit bottom, set delta to zero
          if self.colour[index] < DIM:
             self.delta_colour[index] = 0


   def Brightness_Up(self):
       # Increase each colour value
       for index in range(RGB):
           self.colour[index] += self.delta_colour[index]

           # When we hit top, stop
           if self.colour[index] >= BRIGHT:
               self.delta_colour[index] = -CHANGE_COLOUR



   def Adjust_Colour(self):
       # See if we should adjust brightness up or down
       up_down = 0
       for index in range(RGB):
           up_down += self.delta_colour[index]

       # Shift brightness down
       if up_down < 0:
          self.Brightness_Down()
       # Shift brightness up
       elif up_down > 0:
          self.Brightness_Up()
       # We are stuck, go to the next colour
       else:
          self.Change_Colour()

   
def signal_handler(my_signal, temp):
   sense.clear()
   sys.exit(0)

def main():
   signal.signal(signal.SIGINT, signal_handler)
   sense.set_rotation(180)
   sense.set_pixels(tree)
   lights = []
   my_light = Light(4, 2)
   lights.append(my_light)
   my_light = Light(3, 3)
   lights.append(my_light)
   my_light = Light(5, 4)
   lights.append(my_light)
   my_light = Light(2, 5)
   lights.append(my_light)
   my_light = Light(6, 5)
   lights.append(my_light)

   while True:
      for my_light in lights:
          x = my_light.Get_X()
          y = my_light.Get_Y()
          colour = my_light.Get_Colour()
          sense.set_pixel(x, y, colour)
          my_light.Adjust_Colour()
 
      time.sleep(TIME_DELAY)



if __name__ == "__main__":
   main()

