from sense_hat import SenseHat

sense = SenseHat()
my_colour = [0, 100, 0]

# Read air pressure from the Sense HAT's barometer in mbar
pressure = sense.get_pressure()
# Convert to kPa
pressure = round(pressure / 10, 2)
pressure_message = str(pressure) + " kpa"
sense.set_rotation(180)
sense.clear()
sense.show_message( pressure_message, text_colour=my_colour)
sense.clear()

