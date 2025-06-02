# SenseHAT

This repository hosts a series of simple Python scripts which can be
used to interact with the Sense HAT for a Raspberry Pi computer.

## Clear

The Clear program (clear.py) causes the LED lights on the Sense HAT to
flash red, blue, then green. Each colour is displayed for one second.
Then the screen clears. This can be useful for either testing the LED lights
or clearing old display data off the LEDs.



## Clock

The Clock program (clock.py) checks the current time and displays it in
digital numerals on the LED screen of the Sense HAT. The Clock program
updates the time (displayed in 24 hour format) every second, showing
hours in green and minutes in red. The Clock program runs until it
is terminated, usually by pressing Ctrl-C.

The Clock program will change the colour of the digits on the LED
display once per hour.

The Clock program accepts one parameter. By default the clock displays
time in a 24 hour format (13:45). Passing the parameter "12" on the 
command line will cause the clock to display time in a 12 hour format (1:45).



## Compass

The Compass (compass.py) program reads the current direction of the Sense HAT
(assuming the USB ports on the Pi are meant to be facing west. The orientation
of the Pi is then printed to the LED lights.


## Dice

The Dice program (dice.py) generates a random dice roll. By default the value
is in the range of 1-6 (for a six-sided die). However, the program can accept
one optional parameter, a number in the range of 3 to 20. This allows the
program to roll a random number for different types of dice.

The result is displayed both on the console and by a number of randomly
coloured dots which appear on the SenseHAT. The dots remain on the SenseHAT
under the user presses the Enter key. The display is then cleared.

The dots on the SenseHAT screen will be arranged roughly in a circular
pattern around the centre, attempting to evenly space the dots.



## Eggtimer

The Eggtimer (eggtimer.py) program accepts a single parameter, a time in
seconds. The script then lights up the LED board with a spectrum of colours,
which is displayed in a spiral around the LEDs
.
The lights are then turned off at a rate which will cause the LED board to
go completely dark after the specified number of seconds.

There are 8 colours displyed on the 64 pixel LED board. Specifying a delay
of 64 seconds would cause one light to go out every second. Specifying 32 seconds
would cause two lights to go dark every second. A delay of 192 seconds (just
over three minutes) makes one LED go dark every three seconds.



## Fuzzy

The Fuzzy Python script (fuzzy.py) draws randomly coloured dots at random positions
on the LED screen of the Sense HAT. It draws a new dot every quarter of a second.
Over time, this fills the LED board and gives it a fuzzy/shimmering quality.
The script concludes and clears the screen when Ctrl-C is pressed.


## Heart

The Hear program (heart.py) displays a red heart shape on a blue background
on the Sense HAT's LED display. The image remains for five minutes. Then
the LED screen is cleared/turned off.


## Heat Colours

The Heat Colours Python script (heat-colours.py) begins by setting the LED display
to show green on all pixels. The script then begins monitoring the temperature around the
Sense HAT. As the temperature rises, the LED display shifts its colours along the
spectrum toward red (yellow, orange, then red). If the temperature lowers, the
colours shift toward purple (teal, blue, purple).

The script continues to check for changes in temperature until terminated or
interrupted with Ctrl-C.

The idea behind Heat Colours was to give a quick visual indicator if a task running
on the Raspberry Pi was making the air around it warmer. Running Heat Colours in the
background gives immediate feedback on the air temperature near the Pi without needing
to run other tools like system monitors or the sensors program.


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



## Memory

The Memory script (memory.py) implements a simple memory game using colours.
The LED screen is divided into nine squares, with the eight squares around
the outside each assigned a colour.

The game selects a series of colours at random. Each round the player is shown
a sequence of colours, in order. Once each colour has flashed, in sequence,
the player uses the Sense HAT's joystick to select those same colours in
the same order.

When the player successfully picks the right sequence of colours, the
game flashes a green light in the middle of the LED display. Then 
the player is shown a new, longer sequence of colours and the player
needs to input the new sequence.

During the first round the player needs to remember one colour. Then
two colours in the second round, then three in the third, and so on.

When the player guesses a colour incorrectly the game is over and Memory
will display how many rounds the player completed on the LED screen.



## Nibbles

The Nibbles (nibbles.py) program is a small scale recreation of the classic
"Snake" game or QBASIC's "Nibbles". The player uses the Sense HAT's joystick
to direct a yellow snake around the screen. The snake starts small (just two
pixels). Each time the snake runs into a piece of food (represented by a green
pixel) the snake grows.

The object of the game is to grow the snake as large as possible by eating food
while not running into the sides of the screen. The snake also cannot run into
(or eat) itself or it will die and the game will be over.

The joystick turns the snake. Pressing "down" on the joystick pauses
(and unpauses) the game.



## Nightlight

The Nightlight (nightlight.py) program detects when there is little to no light
in the room. It then displays colours on the LED display, cycling through the
spectrum. Colours gradually shift through shades between colours, slowly
adjusting from green to teal, then blue, purple, red, orange, yellow, and back to green.
The visual sensor tries to detect light in the room and the script turns off
the LEDs if bright light is detected.

The lightnight can also be stopped by pressing Ctrl-C which turns off the LEDs.



## Pressure

The Pressure program (pressure.py) detects the current air pressure
(assuming the Sense HAT has been calibrated) and displays the 
air pressure level on the LED screen. The pressure is displayed
in kpa (one-tenth of a mbar).


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



## Christmas Tree

The Christmas Tree program (tree.py) displays a small evergreen tree on the Sense HAT's
LED display. Randomly coloured lights appear on the tree and slowly grow brighter and
dimmer, changing colours each bright/dim cycle. The lights continue to change colours
and brightness until Ctrl-C is pressed.

