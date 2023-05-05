_B=False
_A=True
MAZE_LEVELS=[[[1,1,1,1,1,0,1,1,1,1,1],[1,0,0,0,1,0,1,0,0,0,0],[1,0,1,1,1,0,1,1,1,1,1],[1,0,1,0,0,0,0,0,0,0,1],[1,0,1,1,1,0,1,1,1,1,1],[1,0,0,0,1,0,1,0,0,0,1],[1,0,1,1,1,1,1,0,1,1,1],[1,0,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,0,1,1,2,0,1],[1,0,0,0,1,0,1,0,0,0,1],[1,1,1,0,1,1,1,0,1,1,1]]]
MAZE_DISPLAY_LEVELS=[[[2,5,2,3],[2,5,1,6]],[[1,5,4,2],[2,4,2,5]],[[2,6,4,4],[2,5,4,6]],[[3,7,1,4],[3,5,1,1]],[[2,4,6,3],[1,5,4,5]],[[2,4,5,1],[2,1,3,5]],[[5,2,1,6],[5,2,2,2]],[[3,2,4,1],[3,3,3,4]],[[6,3,5,2],[5,1,1,3]]]
SOLVED=_B
countdwonTime=5*60*1000
tm=TM1637.create(DigitalPin.P12,DigitalPin.P2,7,4)
tm.show_dp(0,_A)
tm.show_dp(1,_A)
tm.show_dp(2,_A)
tm.show_dp(3,_A)
tm.show_dp(4,_A)
tm.show_dp(5,_A)
tm.show_dp(6,_A)
countdownIsRunning=_B
mazeCurrentLevel=0
mazeCurrentX=0
mazeCurrentY=0
mazeModuleDefused=_B
SHIFT=_B
pixels=neopixel.create(DigitalPin.P0,64,NeoPixelMode.RGB)
pixels.set_brightness(20)
pixels.show()
cWhite=neopixel.colors(NeoPixelColors.WHITE)
cRed=neopixel.colors(NeoPixelColors.RED)
cGreen=neopixel.colors(NeoPixelColors.GREEN)
cBlue=neopixel.colors(NeoPixelColors.BLUE)
cClear=neopixel.colors(NeoPixelColors.BLACK)
pins.set_pull(DigitalPin.P8,PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P16,PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P15,PinPullMode.PULL_UP)
pins.set_pull(DigitalPin.P9,PinPullMode.PULL_UP)
def on_pulsed_p8_low():
	global countdownIsRunning
	if countdownIsRunning:mazeTryToMove(0,1);mazePrintLevel();mazeShowPlayer()
	else:initGame();countdownIsRunning=_A
	pause(100)
def on_pulsed_p16_low():
	global countdownIsRunning
	if countdownIsRunning:mazeTryToMove(-1,0);mazePrintLevel();mazeShowPlayer()
	else:initGame();countdownIsRunning=_A
	pause(100)
def on_pulsed_p15_low():
	global countdownIsRunning
	if countdownIsRunning:mazeTryToMove(1,0);mazePrintLevel();mazeShowPlayer()
	else:initGame();countdownIsRunning=_A
	pause(100)
def on_pulsed_p9_low():
	global countdownIsRunning
	if countdownIsRunning:mazeTryToMove(0,-1);mazePrintLevel();mazeShowPlayer()
	else:initGame();countdownIsRunning=_A
	pause(100)
def printDebug():serial.write_line('mazeMap:'+mazeGetLevelAtPos(mazeCurrentY,mazeCurrentX,mazeCurrentLevel)+'¦ shift:'+SHIFT+'¦x2 Y:'+mazeCurrentY+' X:'+mazeCurrentX)
def mazeGetLevelAtPos(y,x,level):return MAZE_LEVELS[level][y-2][x-2]
def mazeHidePlayer():showPixelOnMatrix(mazeCurrentY,mazeCurrentX,cClear)
def mazeShowPlayer():showPixelOnMatrix(mazeCurrentY,mazeCurrentX,cBlue)
def mazeTryToMove(moveY,moveX):
	D=moveX;C=moveY;global mazeCurrentX;global mazeCurrentY;mazeHidePlayer();A=mazeCurrentX+D;B=mazeCurrentY+C;serial.write_line('possy: '+B+' possx: '+A);E=A<=1 or B<=1 or A>12 or B>12;serial.write_line('outOfBox: '+E);printDebug()
	if not E:
		serial.write_line('levelAt: '+mazeGetLevelAtPos(B,A,mazeCurrentLevel))
		if mazeGetLevelAtPos(B,A,mazeCurrentLevel)==0:pixels.show_color(cRed);pause(2000);pixels.clear();drawWalls();mazePrintLevel()
		else:mazeCurrentY=B+C;mazeCurrentX=A+D;mazeCheckWin();printDebug()
	else:pixels.show_color(cRed);pause(2000);pixels.clear();drawWalls();mazePrintLevel()
def millisToTime(millis):A=millis//1000;B=A//60;C=A%60;return B,C
def onEvery_interval():
	global countdwonTime
	if countdownIsRunning:countdwonTime-=1000
	if not SOLVED:A,B=millisToTime(countdwonTime);tm.show_number(A*100+B);tm.show_dp(1,_A)
loops.every_interval(1000,onEvery_interval)
def drawWalls():
	A=[0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63]
	for B in A:pixels.set_pixel_color(B,cWhite)
def showPixelOnMatrix(y,x,color):
	y/=2;x/=2;x+=1;y+=1;serial.write_line('x: '+x+' y: '+y)
	if y>8 or x>8:print('row or column to big (max 8)')
	else:A=x+8*(y-1)-1;pixels.set_pixel_color(A,color);pixels.show()
def mazePrintLevel():
	B=[cBlue,cRed,cGreen,cGreen]
	for A in range(1,4):C=MAZE_DISPLAY_LEVELS[mazeCurrentLevel][0][A]*2;D=MAZE_DISPLAY_LEVELS[mazeCurrentLevel][1][A]*2;showPixelOnMatrix(C,D,B[A])
def mazeInitLevel():global mazeCurrentX;global mazeCurrentY;mazeCurrentY=MAZE_DISPLAY_LEVELS[mazeCurrentLevel][0][0]*2;mazeCurrentX=MAZE_DISPLAY_LEVELS[mazeCurrentLevel][1][0]*2
def initGame():global mazeCurrentLevel;mazeCurrentLevel=0;drawWalls();mazeInitLevel();mazePrintLevel();mazeShowPlayer();pixels.show()
def mazeCheckWin():
	if mazeGetLevelAtPos(mazeCurrentY,mazeCurrentX,mazeCurrentLevel)==2:pixels.clear();pixels.show_color(cGreen);pixels.show();global SOLVED;SOLVED=_A;A=_B
def on_forever():
	if pins.digital_read_pin(DigitalPin.P16)==0:on_pulsed_p16_low()
	if pins.digital_read_pin(DigitalPin.P15)==0:on_pulsed_p15_low()
	if pins.digital_read_pin(DigitalPin.P9)==0:on_pulsed_p9_low()
	if pins.digital_read_pin(DigitalPin.P8)==0:on_pulsed_p8_low()
basic.forever(on_forever)