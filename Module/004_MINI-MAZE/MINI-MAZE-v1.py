#from microbit import *

MAZE_LEVELS = [
    [  # Level 00
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 2, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    ],
    [  # Level 01
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 2, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        ],
]

MAZE_DISPLAY_LEVELS = [
    [ # Level 00
        [2, 5, 2, 3],
        [2, 5, 1, 6],
    ],
    [ # Level 01
        [1, 5, 4, 2],
        [2, 4, 2, 5],
    ],
    [ # Level 02
        [2, 6, 4, 4],
        [2, 5, 4, 6],
    ],
    [ # Level 03
        [3, 7, 1, 4],
        [3, 5, 1, 1],
    ],
    [ # Level 04
        [2, 4, 6, 3],
        [1, 5, 4, 5],
    ],
    [ # Level 05
        [2, 4, 5, 1],
        [2, 1, 3, 5],
    ],
    [ # Level 06
        [5, 2, 1, 6],
        [5, 2, 2, 2],
    ],
    [ # Level 07
        [3, 2, 4, 1],
        [3, 3, 3, 4],
    ],
    [ # Level 08
        [6, 3, 5, 2],
        [5, 1, 1, 3],
    ]
]
### Game Variables
SOLVED = False

### Countdown Variables
countdwonTime = 5 * 60 * 1000
tm = TM1637.create(DigitalPin.P12, DigitalPin.P2, 7, 4)
tm.show_dp(1, True)
countdownIsRunning = False

### Maze Variables
mazeCurrentLevel = 0
mazeCurrentX = 0
mazeCurrentY = 0
mazeModuleDefused = False

SHIFT = False ### Microbit testing only

### NeoPixel
#LED_BRIGHTNESS = 0.5
pixels = neopixel.create(DigitalPin.P0, 64, NeoPixelMode.RGB)
pixels.set_brightness(20)
pixels.show()

### COLORS
cWhite = neopixel.colors(NeoPixelColors.WHITE)
cRed = neopixel.colors(NeoPixelColors.RED)
cGreen = neopixel.colors(NeoPixelColors.GREEN)
cBlue = neopixel.colors(NeoPixelColors.BLUE)
cClear = neopixel.colors(NeoPixelColors.BLACK)

### Buttons
pins.set_pull(DigitalPin.P8, PinPullMode.PULL_UP) # right
pins.set_pull(DigitalPin.P16, PinPullMode.PULL_UP) # up
pins.set_pull(DigitalPin.P15, PinPullMode.PULL_UP) # down
pins.set_pull(DigitalPin.P9, PinPullMode.PULL_UP) # left
 

def on_pulsed_p8_low():
    global countdownIsRunning
    if countdownIsRunning:
        mazeTryToMove(0, 1) # Right
        mazePrintLevel()
        mazeShowPlayer()
    else:
        initGame()
        countdownIsRunning = True
    pause(100)

def on_pulsed_p16_low():
    global countdownIsRunning
    if countdownIsRunning:
        mazeTryToMove(-1, 0) # up
        mazePrintLevel()
        mazeShowPlayer()
    else:
        initGame()
        countdownIsRunning = True
    pause(100)

def on_pulsed_p15_low():
    global countdownIsRunning
    if countdownIsRunning:
        mazeTryToMove(1, 0) # down
        mazePrintLevel()
        mazeShowPlayer()
    else:
        initGame()
        countdownIsRunning = True
    pause(100)

def on_pulsed_p9_low():
    global countdownIsRunning
    if countdownIsRunning:
        mazeTryToMove(0, -1) # left
        mazePrintLevel()
        mazeShowPlayer()
    else:
        initGame()
        countdownIsRunning = True
    pause(100)

def printDebug():
    serial.write_line("mazeMap:" + mazeGetLevelAtPos(mazeCurrentY, mazeCurrentX, mazeCurrentLevel) + "¦ shift:" + SHIFT + "¦x2 Y:" + mazeCurrentY +" X:"+ mazeCurrentX)

def mazeGetLevelAtPos(y,x, level):
    return MAZE_LEVELS[level][y-2][x-2]

def mazeHidePlayer():
    showPixelOnMatrix(mazeCurrentY, mazeCurrentX, cClear)

def mazeShowPlayer():
    showPixelOnMatrix(mazeCurrentY, mazeCurrentX, cBlue)

def mazeTryToMove(moveY, moveX):
    global mazeCurrentX
    global mazeCurrentY
    
    mazeHidePlayer()
    mazePossibleX = mazeCurrentX + moveX
    mazePossibleY = mazeCurrentY + moveY
    #serial.write_line("possy: " + mazePossibleY + " possx: " + mazePossibleX)
    outOfBox = mazePossibleX <= 1 or mazePossibleY <= 1 or mazePossibleX > 12 or mazePossibleY > 12
    #serial.write_line("outOfBox: "+ outOfBox)

    printDebug()
    if not outOfBox:
        #serial.write_line("levelAt: "+mazeGetLevelAtPos(mazePossibleY, mazePossibleX, mazeCurrentLevel))
        if mazeGetLevelAtPos(mazePossibleY, mazePossibleX, mazeCurrentLevel) == 0:
            #music.play_melody("B G A E F ", 120)
            error()
        else:
            mazeCurrentY = mazePossibleY + moveY #The move has to be applied twice in "big" coords
            mazeCurrentX = mazePossibleX + moveX
            mazeCheckWin()
    else:
        error()

def error():
    global countdwonTime
    pixels.show_color(cRed)
    if countdwonTime>=60000:
        countdwonTime -= 60000
    else:
        countdwonTime = 0
    pause(2000)
    pixels.clear()
    drawWalls()
    mazePrintLevel()

def millisToTime(millis):
    TotalSeconds = millis // 1000
    minutes = TotalSeconds // 60
    seconds = TotalSeconds % 60
    return minutes, seconds


def onEvery_interval():
    global countdwonTime
    if countdownIsRunning and countdwonTime > 0:
        countdwonTime -= 1000
    if not SOLVED:
        minutes, seconds = millisToTime(countdwonTime)
        tm.show_number(minutes * 100 + seconds)
        tm.show_dp(1, True)

        
loops.every_interval(1000, onEvery_interval)
def drawWalls():
    walls = [0, 1, 2, 3, 4, 5, 6, 7, 8,
            15, 16, 23, 24, 31, 32, 39,
            40, 47, 48, 55, 56, 57, 58,
            59, 60, 61, 62, 63]
    for NeoPixelLed in walls:
        pixels.set_pixel_color(NeoPixelLed,cWhite)


def showPixelOnMatrix(y, x, color):
    y /= 2
    x /= 2
    x += 1
    y += 1
    serial.write_line("x: " + x + " y: " +y)
    if y > 8 or x > 8:
        print('row or column to big (max 8)')
    else:
        lednumber = x + (8 * (y - 1)) -1
        pixels.set_pixel_color(lednumber, color)
        pixels.show()

def mazePrintLevel():  # displays displays the red and the two green dots
    colors = [cBlue, cRed, cGreen, cGreen]
    for point in range(1, 4):
        pointY = MAZE_DISPLAY_LEVELS[mazeCurrentLevel][0][point]*2
        pointX = MAZE_DISPLAY_LEVELS[mazeCurrentLevel][1][point]*2
        showPixelOnMatrix(pointY, pointX, colors[point])
    

def mazeInitLevel():
    global mazeCurrentX
    global mazeCurrentY
    mazeCurrentY = MAZE_DISPLAY_LEVELS[mazeCurrentLevel][0][0]*2
    mazeCurrentX = MAZE_DISPLAY_LEVELS[mazeCurrentLevel][1][0]*2


def initGame():
    global mazeCurrentLevel
    mazeCurrentLevel = randint(0, 1)
    drawWalls()
    mazeInitLevel()
    mazePrintLevel()
    mazeShowPlayer()
    pixels.show()

def mazeCheckWin():
    if mazeGetLevelAtPos(mazeCurrentY, mazeCurrentX, mazeCurrentLevel) == 2:
        pixels.clear()
        pixels.show_color(cGreen)
        pixels.show()
        global SOLVED
        SOLVED = True
        global countdownIsRunning
        countdownIsRunning = False

def on_forever():
    if (pins.digital_read_pin(DigitalPin.P16)==0):
        on_pulsed_p16_low()
    if (pins.digital_read_pin(DigitalPin.P15)==0):
        on_pulsed_p15_low()
    if (pins.digital_read_pin(DigitalPin.P9)==0):
        on_pulsed_p9_low()
    if (pins.digital_read_pin(DigitalPin.P8)==0):
        on_pulsed_p8_low()
    if countdwonTime <= 0:
        global countdownIsRunning
        countdownIsRunning = False
        pixels.show_color(cRed)
        pause(2000)


basic.forever(on_forever)