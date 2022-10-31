import board
import time
import neopixel
from random import randrange
from digitalio import DigitalInOut, Direction, Pull

# BUTTONS FOR MOVEMENT
PIN_MAZE_UP = DigitalInOut(board.GP6)
PIN_MAZE_UP.direction = Direction.INPUT
PIN_MAZE_UP.pull = Pull.UP

PIN_MAZE_RIGHT = DigitalInOut(board.GP21)
PIN_MAZE_RIGHT.direction = Direction.INPUT
PIN_MAZE_RIGHT.pull = Pull.UP

PIN_MAZE_LEFT = DigitalInOut(board.GP2)
PIN_MAZE_LEFT.direction = Direction.INPUT
PIN_MAZE_LEFT.pull = Pull.UP

PIN_MAZE_DOWN = DigitalInOut(board.GP13)
PIN_MAZE_DOWN.direction = Direction.INPUT
PIN_MAZE_DOWN.pull = Pull.UP

debounce = 0.3

# Pins for fail or win
PIN_WIN = DigitalInOut(board.GP8)
PIN_WIN.direction = Direction.OUTPUT
PIN_WIN.value = False

PIN_FAIL = DigitalInOut(board.GP9)
PIN_FAIL.direction = Direction.OUTPUT
PIN_FAIL.value = False

# button default states
mazeButtonLeftState = 0        # current state of the left button
mazeButtonRightState = 0       # current state of the right button
mazeButtonUpState = 0          # current state of the up button
mazeButtonDownState = 0        # current state of the down button
lastMazeButtonUpState = PIN_MAZE_UP.value    # previous state of the left button
lastMazeButtonRightState = PIN_MAZE_RIGHT.value   # previous state of the right button
lastMazeButtonLeftState = PIN_MAZE_LEFT.value      # previous state of the up button
lastMazeButtonDownState = PIN_MAZE_DOWN.value    # previous state of the down button

# LED MATRIX
NUM_LED = 64
PIN_LED = board.GP0
LED_BRIGHTNESS = 0.5

MATRIX_ROWS = 8
MATRIX_COLUMNS = 8

# ROWS AND COLUMNS FOR MOVEMENT AND GAMEPLAY
MAZE_LEVEL_ROWS = 13
MAZE_LEVEL_COLUMNS = MAZE_LEVEL_ROWS

# ROWS AND COLUMNS FOR DISPLAYING ON LED MATRIX
MAZE_DISPLAY_LEVEL_ROW = 8
MAZE_DISPLAY_LEVEL_COLUMNS = MAZE_DISPLAY_LEVEL_ROW

# MAZE LEVELS...
# 'c' = green circle positions
# 's' = start position
# 'f' = finish position
# 'X' = wall
# ' ' = movement zone

# ...for movement and gameplay
MAZE_LEVELS = [
    [  # Level 00
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'c', 'X', 's', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 'c', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', 'f', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 01
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', 's', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'c', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', 'c', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'f', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 02
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', 's', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'c', 'X', ' ', 'X', 'c', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'f', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 03
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'c', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', 's', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', 'c', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', 'X', 'f', ' ', ' ', 'X', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 04
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', 's', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'c', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'f', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'c', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 05
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', 'c', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X'],
        ['X', 'f', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'X', 'c', 'X', ' ', 'X', ' ', ' ', 's', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 06
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', 'c', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'f', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 's', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', ' ', 'c', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 07
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'c', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'f', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', 's', ' ', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', ' ', 'c', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [  # Level 08
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', 'c', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
        ['X', 'f', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
        ['X', 'c', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
        ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 's', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ]
]

# ...for displaying on led matrix
MAZE_DISPLAY_LEVELS = [
    [ # Level 00
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'c', 's', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', 'c', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'f', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 01
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 's', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'c', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'c', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'f', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 02
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 's', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'c', ' ', 'c', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'f', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 03
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'c', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', 's', ' ', ' ', ' ', 'X'],
        ['X', 'c', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'f', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 04
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 's', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'c', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'f', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', 'c', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 05
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', 'c', ' ', 'X'],
        ['X', ' ', 's', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'f', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', 'c', ' ', ' ', 's', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 06
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', 'c', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', 'f', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 's', ' ', 'X'],
        ['X', ' ', 'c', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 07
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', 'c', ' ', ' ', 'X'],
        ['X', ' ', ' ', 'f', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', 's', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', 'c', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ],
    [ # Level 08
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', '', 'c', ' ', ' ', ' ', 'X'],
        ['X', 'f', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', 'c', ' ', ' ', ' ', ' ', ' ', 'X'],
        ['X', ' ', ' ', ' ', ' ', 's', ' ', 'X'],
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ]
]

# GAMEPLAY VARIABLES
mazeCurrentLevel = 0 # Current level (0-8) playing
mazeCurrentX = 0 # Current player X position
mazeCurrentY = 0 # Current player Y position
mazeStartX = 0 # Current level start X position
mazeStartY = 0 # Current level start Y position
mazeFinishX = 0 # Current level finish X position
mazeFinishY = 0 # Current level finish Y position
mazeDisplayCurrentX = 0 # Current player X DISPLAY position
mazeDisplayCurrentY = 0 # Current player Y DISPLAY position
mazeDisplayStartX = 0 # Current DISPLAY level start X position
mazeDisplayStartY = 0 # Current DISPLAY level start Y position
mazeDisplayFinishX = 0 # Current level finish X position
mazeDisplayFinishY = 0 # Current level finish Y position
mazeModuleDefused = False
mazeModuleFailed = False
numberOfStrikes = 0
cRed   = (30, 0, 0)
cGreen = (0, 30, 0)
cBlue = (0, 0, 30)
cWhite = (15, 15, 15)
cClear = (0 ,0 ,0) 

def mazePrintLevel():  # displays the 8x8 maze on the led matrix
    for x in range(MAZE_DISPLAY_LEVEL_ROW):
        for y in range(MAZE_DISPLAY_LEVEL_COLUMNS):
            # display the green circles
            if MAZE_DISPLAY_LEVELS[mazeCurrentLevel][x][y] == 'c':
                #print('08: green circle', y, x)
                showPixelOnMatrix(y, x, cGreen)
            # display the finish point
            elif MAZE_DISPLAY_LEVELS[mazeCurrentLevel][x][y] == 'f':
                #print('08: finish point', y, x)
                showPixelOnMatrix(y, x, cRed)

def clearMatrix():
    global cBlue
    cBlue = (0,0,0)    
    pixels.fill((0,0,0))

def mazeInitLevel():
    # sets startX, startY, finishX and finishY for MOVEMENT/ PLAY
    for x in range(MAZE_LEVEL_ROWS):
        for y in range(MAZE_LEVEL_COLUMNS):
            if MAZE_LEVELS[mazeCurrentLevel][x][y] == 's':
                mazeStartX = x
                mazeStartY = y
                #print('16: Start position', mazeStartY, mazeStartX)
            elif MAZE_LEVELS[mazeCurrentLevel][x][y] == 'f':
                mazeFinishX = x
                mazeFinishY = y
                #print('16: Finish position', mazeFinishY, mazeFinishX)

    # sets startX, startY, finishX and finishY for DISPLAY
    for x in range(MAZE_DISPLAY_LEVEL_ROW):
        for y in range(MAZE_DISPLAY_LEVEL_COLUMNS):
            if MAZE_DISPLAY_LEVELS[mazeCurrentLevel][x][y] == 's':
                mazeDisplayStartX = x
                mazeDisplayStartY = y
                #print('08: Start Position', mazeDisplayStartY, mazeDisplayStartX)
            if MAZE_DISPLAY_LEVELS[mazeCurrentLevel][x][y] == 'f':
                mazeDisplayFinishX = x
                mazeDisplayFinishY = y
                #print('08: Finish Position',
                mazeDisplayFinishY, mazeDisplayFinishX

    global mazeDisplayCurrentX
    global mazeDisplayCurrentY
    global mazeCurrentX
    global mazeCurrentY

    mazeCurrentX = mazeStartX
    mazeCurrentY = mazeStartY
    mazeDisplayCurrentX = mazeDisplayStartX
    mazeDisplayCurrentY = mazeDisplayStartY

    mazePrintLevel()

def mazeShowPlayer():
    showPixelOnMatrix(mazeDisplayCurrentY, mazeDisplayCurrentX, cBlue)

def mazeHidePlayer():
    showPixelOnMatrix(mazeDisplayCurrentY, mazeDisplayCurrentX, cClear)

def mazeCheckWin():
    if MAZE_LEVELS[mazeCurrentLevel][mazeCurrentX][mazeCurrentY] =='f':
        PIN_WIN.value = True
        clearMatrix()
        global mazeModuleDefused
        mazeModuleDefused = True


def addStrike():
    global numberOfStrikes
    global mazeModuleFailed

    numberOfStrikes += 1

    pixels.fill(cRed)

    PIN_FAIL.value = True
    time.sleep(1)
    PIN_FAIL.value = False

    pixels.fill((0,0,0))


    if numberOfStrikes == 1:
        print('num of strikes:', numberOfStrikes)
        print('module failed:', mazeModuleFailed)
        initGame()
    elif numberOfStrikes == 2:
        print('num of strikes:', numberOfStrikes)
        print('module failed:', mazeModuleFailed)
        initGame()
    elif numberOfStrikes == 3:
        print('num of strikes:', numberOfStrikes)
        mazeModuleFailed = True
        print('module failed:', mazeModuleFailed)


# Tries to move the player to a given direction.
# The movement is allowed based on MIN_CURRENT and MAX_CURRENT values
# and also if the desired movement is towards an allowed movement placed, i.e. 'X', 's', 'f'
# Returns true if the movement was successful, otherwise false

def mazeTryToMove(movement):
    global mazeCurrentX
    global mazeCurrentY
    global mazeDisplayCurrentX
    global mazeDisplayCurrentY

    mazePossibleX = mazeCurrentX
    mazePossibleY = mazeCurrentY
    if movement == 'Left':
        print('movement LEFT')
        mazeHidePlayer()
        mazePossibleY -= 1
        # Checks what would happen if we apply the possible new position
        if MAZE_LEVELS[mazeCurrentLevel][mazePossibleX][mazePossibleY] != 'X':
            mazeCurrentY = mazePossibleY - 1
            mazeDisplayCurrentY = mazeDisplayCurrentY - 1
        else:
            addStrike()
            mazeShowPlayer()
            mazeCheckWin()
   
    elif movement == 'Right':
        print('movement RIGHT')
        mazeHidePlayer()
        mazePossibleY += 1
        # Checks what would happen if we apply the possible new position
        if MAZE_LEVELS[mazeCurrentLevel][mazePossibleX][mazePossibleY] != 'X':
            mazeCurrentY = mazePossibleY + 1
            mazeDisplayCurrentY += 1
        else:
            addStrike()
            mazeShowPlayer()
            mazeCheckWin()
    
    elif movement == 'Up':
        print('movement UP')
        mazeHidePlayer()
        mazePossibleX -= 1
        # Checks what would happen if we apply the possible new position
        if MAZE_LEVELS[mazeCurrentLevel][mazePossibleX][mazePossibleY] != 'X':
            mazeCurrentX = mazePossibleX - 1
            mazeDisplayCurrentX = mazeDisplayCurrentX - 1
        else:
            addStrike()
            mazeShowPlayer()
            mazeCheckWin()
    
    elif movement == 'Down':
        print('movement DOWN')
        mazeHidePlayer()
        mazePossibleX += 1
        # Checks what would happen if we apply the possible new position
        if MAZE_LEVELS[mazeCurrentLevel][mazePossibleX][mazePossibleY] != 'X':
            mazeCurrentX = mazePossibleX + 1
            mazeDisplayCurrentX = mazeDisplayCurrentX + 1
        else:
            addStrike()
            mazeShowPlayer()
            mazeCheckWin()

def drawWalls():
    walls = [0, 1, 2, 3, 4, 5, 6, 7, 8,
            15, 16, 23, 24, 31, 32, 39,
            40, 47, 48, 55, 56, 57, 58,
            59, 60, 61, 62, 63]

    for led in walls:
        pixels[led] = cWhite

def showPixelOnMatrix(column, row, color):
    # LED Numbers of Matrix 8x8
    # 00 01 02 03 04 05 06 07
    # 08 09 10 11 12 13 14 15
    # 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31
    # 32 33 34 35 36 37 38 39
    # 40 41 42 43 44 45 46 47
    # 48 49 50 51 52 53 54 55
    # 56 57 58 59 60 61 62 63
    #
    # ex. row = 4 col = 6 -> LED 29
    row += 1
    column += 1

    if row > 8 or column > 8:
        print('row or column to big (max 8)')
    else:
        lednumber = column + (8 * (row -1)) -1
        pixels[lednumber] = color

def printDebug():
    print("mazeModuleDefused:", mazeModuleDefused, "¦ level:", mazeCurrentLevel, "¦ 16:",mazeCurrentY, mazeCurrentX, "¦ 08 Y X:", mazeDisplayCurrentY, mazeDisplayCurrentX)
    print("wait for userinput...")

def initGame():
    global mazeCurrentLevel
    mazeCurrentLevel = randrange(8)

    drawWalls()
    mazeInitLevel()
    mazeShowPlayer()

# ----- SETUP -----
pixels = neopixel.NeoPixel(PIN_LED, NUM_LED)
pixels.brightness = LED_BRIGHTNESS

pixels.fill((0,0,0))
time.sleep(2)

initGame()
pixels.show()


# ----- LOOP -----
while True:
    mazeCheckWin()

    if mazeModuleDefused != True and mazeModuleFailed != True:
        currentMazeButtonStateRight = PIN_MAZE_RIGHT.value
        currentMazeButtonStateLeft = PIN_MAZE_LEFT.value
        currentMazeButtonStateUp = PIN_MAZE_UP.value
        currentMazeButtonStateDown = PIN_MAZE_DOWN.value


        if currentMazeButtonStateRight != lastMazeButtonRightState:
            if not currentMazeButtonStateRight:
                mazeTryToMove("Right")
                mazePrintLevel()
                time.sleep(debounce)
            
            lastMazeButtonRightState = currentMazeButtonStateRight

        elif currentMazeButtonStateLeft != lastMazeButtonLeftState:
            if not currentMazeButtonStateLeft:
                mazeTryToMove("Left")
                mazePrintLevel()
                time.sleep(debounce)
            
            lastMazeButtonLeftState = currentMazeButtonStateLeft
        
        elif currentMazeButtonStateUp != lastMazeButtonUpState:
            if not currentMazeButtonStateUp:
                mazeTryToMove("Up")
                mazePrintLevel()
                time.sleep(debounce)
            
            lastMazeButtonUpState = currentMazeButtonStateUp
            
        elif currentMazeButtonStateDown != lastMazeButtonDownState:
            if not currentMazeButtonStateDown:
                mazeTryToMove("Down")
                mazePrintLevel()
                time.sleep(debounce)
            
            lastMazeButtonDownState = currentMazeButtonStateDown
            
        mazeShowPlayer()

        pixels.show()
    elif mazeModuleFailed == True:
        pixels.fill(cRed)
    elif mazeModuleDefused == True:
        pixels.fill((0,0,0))