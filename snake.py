#!/bin/env python

import curses
import os
import sys
import time
from time import sleep
from random import randint
from settings import RIGHT, LEFT, UP, DOWN, HEAD, BODY, FOOD, ERASE, FOOD_LIMIT, FOOD_TIME, END_LEVEL, RATE, FPS, SNAKE_SPEED, THE_END, X1, Y1, X2, Y2, startX, startY 


def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
     sys.stdout.flush()


def endGame():
    global THE_END
    THE_END = not THE_END


class Position(object):
    def __init__(self, x, y):
        super(Position, self).__init__()
        self.x = x
        self.y = y


class PositionSnake(Position):
    def __init__(self, x, y, direction):
        super(PositionSnake, self).__init__(x, y)
        self.direction = direction


class PositionFood(Position):
    def __init__(self, x, y, ts):
        super(PositionFood, self).__init__(x, y)
        self.timeStamp = ts


class Food():
    def __init__(self):
        self.food = []

    def put(self, snake):
        flag = False
        while not flag:
            x = randint(X1+1, X2-1)
            y = randint(Y1+2, Y2-1)
            same = False
            for s in snake.body:
                if (s.x == x) and (s.y == y):
                   same = True 
            if not same:
               flag = True
        self.food.append(PositionFood(x, y, time.time()))
        print_there(x, y, FOOD)

    def remove(self):
        l = []
        for f in self.food:
            t1 = time.time()
            if ((t1 - f.timeStamp) < FOOD_TIME):
               l.append(f)
            else:
               print_there(f.x, f.y, ERASE)
        self.food = l

    def eraseAll(self):
        for f in self.food:
            print_there(f.x, f.y, ERASE)
        # 
        self.food = []

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

    def hitTheWall(self):
        head = self.body[0]
        if ((head.x == X1+1) or (head.x == X2) or (head.y == Y1+1) or (head.y == Y2+1)):
           sleep(1)
           return True
        return False

    def process_event(self, e):
        firstPart = self.body[0]
        self.moveHere.append(PositionSnake(firstPart.x, firstPart.y, e))

    def eraseAll(self):
        for s in self.body:
            print_there(s.x, s.y, ERASE)
        # 
        s = self.body.pop(0)
        self.body = []
        self.body.append(s)
           

def eatFood(s, f):
    head = s.body[0]
    i = 0
    for food in f.food:
        if (head.x == food.x) and (head.y == food.y):
           f.food.pop(i)
           return True
        i += 1
    return False
        

def realtime(THE_END=False):
    global SNAKE_SPEED

    snake  = Snake()
    food   = Food()

    counter = 0

    level = 1

    while not THE_END:

          print_there(0, Y2+2, 80*ERASE)
          print_there(0, Y2+2, "Level: %d      Points: %d" %(level, len(snake.body)-1))

          snake.move()

          food.remove()

          if eatFood(snake,food):
             snake.grow()

          if snake.hitTheWall():
             THE_END = True

          counter += 1
          if counter > 30:
             counter = 0
             if (len(food.food) < FOOD_LIMIT):
                food.put(snake)               

          char = screen.getch()
          if (char == ord('q')):
             THE_END = True
          elif char in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
             snake.process_event(char)

          #sleep(0.1)
          sleep(FPS / (SNAKE_SPEED * 10.0))

          if (len(snake.body) > END_LEVEL):
             msg = "N  E  W     L  E  V  E  L"
             print_there(int((X2 - X1)/ 2) - int(len(msg))/2,int((Y2 - Y1)/2), msg)
             sleep(3) 
             print_there(int((X2 - X1)/ 2) - int(len(msg))/2,int((Y2 - Y1)/2), int(len(msg))*ERASE)
             #
             snake.eraseAll()
             food.eraseAll()
             SNAKE_SPEED = SNAKE_SPEED + RATE
             level += 1

    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()


#####################################
# BEGIN                             #
#####################################

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
# DRAW FIELD
#
screen.addstr(Y1, X1, (X2-X1)*"-")
for y in range(Y1+1, Y2):
    screen.addstr(y, X1, "|")
    screen.addstr(y, X2-1, "|")
screen.addstr(Y2, X1, (X2-X1)*"-")

if __name__ == '__main__':
   os.system('clear')
   realtime()
