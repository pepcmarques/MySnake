import curses

RIGHT = curses.KEY_RIGHT
LEFT  = curses.KEY_LEFT
UP    = curses.KEY_UP
DOWN  = curses.KEY_DOWN
#
HEAD  = "S"
BODY  = "s"
FOOD  = "*"
ERASE = " "
INITIAL_SIZE = 1   # For testing purpose. You can start each level with a 10 peaces snake for example...
#
FOOD_LIMIT = 4
FOOD_TIME  = 10
END_LEVEL  = 30
#
RATE        = 5.0
FPS         = 30.0
SNAKE_SPEED = 30.0
#
THE_END = False
#
X1 = 0
Y1 = 0
X2 = 80
Y2 = 23
#
startX = int((X2 - X1) / 2)
startY = int((Y2 - Y1) / 2)
