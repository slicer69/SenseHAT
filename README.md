# SenseHAT

This repository hosts a series of simple Python scripts which can be
used to interact with the Sense HAT for a Raspberry Pi computer.

## Clear

The Clear program (clear.py) causes the LED lights on the Sense HAT to
flash red, blue, then green. Each colour is displayed for one second.
Then the screen clears. This can be useful for either testing the LED lights
or clearing old display data off the LEDs.


## Compass

The Compass (compass.py) program reads the current direction of the Sense HAT
(assuming the USB ports on the Pi are meant to be facing west. The orientation
of the Pi is then printed to the LED lights.


## Fuzzy

The Fuzzy Python script (fuzzy.py) draws randomly coloured dots at random positions
on the LED screen of the Sense HAT. It draws a new dot every quarter of a second.
Over time, this fills the LED board and gives it a fuzzy/shimmering quality.
The script concludes and clears the screen when Ctrl-C is pressed.


## Heart

The Hear program (heart.py) displays a red heart shape on a blue background
on the Sense HAT's LED display. The image remains for five minutes. Then
the LED screen is cleared/turned off.


## Hello

The Hello script (hello.py) displays the message "Hello World!" is scrolling
text on the LED display of the Sense HAT.

## Joystick

The Joystick (joystick.py) script can be used to confirm the Sense HAT's joystick
works. When the stick is pushed Up the Sense HAT's LED display is set to red.
Then the stick is pressed Down the lights turn blue. Left causes the lights to
turn yellow and Right turns the lights green.

To exit the test program, depress the joystick. The LED screen will then
be cleared.

Note: The colour of the LEDs will not change until the joystick is released
(when the user stops pushing on it). This is to insure the colour doesn't
keep trying to change over and over while the stick is being pushed.


## Life

The Life script (life.py) implements the classic Game of Life. Cells on the 
LED are lit up at random. Then each cell undergoes a transformation
(reproducing or dying), based on the number of lit up cells around it. 
Then the colour and the new cells are displayed on the LED screen.

The colour and cells change once every two seconds. The game stops when the
joystick button is depressed and released.


## Temp

The Temperature (temp.py) program checks the current room temperature around the
Sense HAT every ten seconds. If the temperature is less than 30C then
the LED display shows the current temperature in blue. When the temperature is
in the range of 30 to 49 degrees the temperature is displayed in green. For any
temperature of 50C or higher the temperature is shown in red on the LED display.

The script runs constantly, every ten seconds, until terminated. The
script can be terminated by presseding Ctrl-C.


# Tic Tac Toe

The Tic Tac Toe script (ttt-hat.py) plays a game of Tic Tac Toe on the LED display.
The 8x8 lights are divided into nine squares (a 3x3 grid). The player moves the
cursor (shown in yellow) with the joystick and depresses the stick to select their
move. Their move is shown in red. The computer then moves, marking their square
with blue. (Note: when the player moves their cursor over an occupied square, the
cursor turns from yellow to purple.)

The game continues until all squares are full or one player wins the game. The
results are then shown in a scrolling text across the LEDs.


Note: ny of the above games or scripts with long delays can be
exited by pressing Ctrl-C on the console. This will cause the
games/demos to clean up the LED display and exit.

