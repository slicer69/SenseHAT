from sense_hat import SenseHat
import time

red = (200, 0, 0)
yellow = (200, 200, 0)
green = (0, 200, 0)
blue = (0, 0, 200)

sense = SenseHat()

finished = False
colour = green

while not finished:
   my_event = sense.stick.wait_for_event(emptybuffer = True)
   if my_event.action == "released":
      if my_event.direction == "up":
         colour = red
      elif my_event.direction == "down":
         colour = blue
      elif my_event.direction == "left":
         colour = yellow
      elif my_event.direction == "right":
         colour = green
      elif my_event.direction == "middle":
         finished = True

      sense.clear(colour)

my_event = sense.stick.get_events()
sense.clear()


