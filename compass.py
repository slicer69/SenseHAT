from sense_hat import SenseHat

sense = SenseHat()

direction = sense.get_compass()
sense.set_rotation(180)
degrees = round(direction)
sense.show_message(str(degrees))

