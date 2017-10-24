#!/bin/env python

import os
import sys
import time
from time import sleep
from random import randint

import os
import curses

# get the curses screen window
screen = curses.initscr()
#
# turn off input echoing
curses.noecho()
#
# respond to keys immediately (don't wait for enter)
screen.nodelay(True)
curses.cbreak()
#
# map arrow keys to special values
screen.keypad(True)
#

RIGHT = curses.KEY_RIGHT
LEFT  = curses.KEY_LEFT
UP    = curses.KEY_UP
DOWN  = curses.KEY_DOWN
ESC   = curses.KEY_EXIT

HEAD  = "S"
BODY  = "s"
FOOD  = "*"
ERASE = " "

global theEnd
theEnd = False

X1 = 1
Y1 = 1
X2 = 78
Y2 = 23

startX = 10
startY = 10

def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
     sys.stdout.flush()

def endGame():
    global theEnd
    theEnd = not theEnd


class Position(object):

    def __init__(self, x, y):
        super(Position, self).__init__()
        self.x = x
        self.y = y


class PositionSnake(Position):

    def __init__(self, x, y, direction):
        super(PositionSnake, self).__init__(x, y)
        self.direction = direction


class Food():

    def __init__(self):
        self.food = []

    def put(self, snake):

        flag = False
        while not flag:
            x = randint(X1+1, X2-1)
            y = randint(Y1+1, Y2-1)
            same = False
            for s in snake.body:
                if (s.x == x) and (s.y == y):
                   same = True 
            if not same:
               flag = True
        self.food.append(Position(x, y))
        print_there(x, y, FOOD)

class snakePart():

    def __init__(self, x, y, direction, part):
        self.x = x
        self.y = y
        self.direction = direction
        self.part = part


class Snake(object):

    def __init__(self):
        self.body = []
        self.moveHere = []
        self.lastDirection = RIGHT
        self.direction = RIGHT
        self.body.append(snakePart(startX, startY, RIGHT, HEAD))

    def grow(self):
        last = self.body[-1]
        x = last.x
        y = last.y
        if last.direction == RIGHT:
            x = x - 1 
        elif last.direction == LEFT:
            x = x + 1
        elif last.direction == UP:
            y = y + 1
        elif last.direction == DOWN:
            y = y - 1
        self.body.append(snakePart(x, y, last.direction, BODY))
        print_there(x, y, BODY)

    def move(self):

        print_there(0, 0, 80*ERASE)
        print_there(0, 0, "Coordinate: %d   Body: %d" %(len(self.moveHere), len(self.body)))

        last = self.body[-1]

        for s in self.body:

            print_there(s.x, s.y, ERASE)

            p = 0
            while p < len(self.moveHere):
                if (s.x == self.moveHere[p].x) and (s.y == self.moveHere[p].y):
                   s.direction = self.moveHere[p].direction
                   if (last.x == s.x) and (last.y == s.y):
                      self.moveHere.pop(p)
                p += 1

            if s.direction == RIGHT:
               s.x = s.x + 1
            elif s.direction == DOWN:
               s.y = s.y + 1
            if s.direction == LEFT:
               s.x = s.x - 1
            elif s.direction == UP:
               s.y = s.y - 1
           
            print_there(s.x, s.y, s.part)


    def process_event(self, e):
        firstPart = self.body[0]
        self.moveHere.append(PositionSnake(firstPart.x, firstPart.y, e))
           

def eatFood(s, f):
    head = s.body[0]
    i = 0
    for food in f.food:
        if (head.x == food.x) and (head.y == food.y):
           f.food.pop(i)
           return True
        i += 1
    return False
        

def realtime(theEnd=False):
    snake  = Snake()
    food   = Food()

    snake.grow()
    snake.grow()

    counter = 0

    while not theEnd:

          snake.move()

          if eatFood(snake,food):
             snake.grow()

          counter += 1
          if counter > 30:
             counter = 0
             food.put(snake)               

          char = screen.getch()
          if (char == ord('q')) or (char == ESC):
             theEnd = True
          elif char in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
             snake.process_event(char)

          sleep(.05)

    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
 
if __name__ == "__main__":
   os.system('clear')
   realtime()
