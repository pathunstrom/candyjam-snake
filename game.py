__author__ = 'Patrick'

import pygame
import sys
from pygame.locals import *
from random import randint

interval = 150
square_size = 10
spaces = 30


class Segment(object):
    """Parent class for Head and Body"""
    def __init__(self):
        self.rect = pygame.Rect(0, 0, square_size, square_size)
        self.old_x = -1
        self.old_y = 0
        self.color = (0, 0, 0)

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect)


class Head(Segment):
    """The snake's head. Collision detection!"""
    def __init__(self):
        super(Head, self).__init__()
        self.x, self.y = 0, 0
        self.vector_x = 1
        self.vector_y = 0
        self.color = (0, 255, 0)

    def move(self):
        self.old_x, self.old_y = self.x, self.y
        self.x += self.vector_x
        self.y += self.vector_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)


class Body(Segment):
    """The Snake's body. Don't bite yourself."""
    def __init__(self, parent):
        super(Body, self).__init__()
        self.parent = parent
        self.x, self.y = parent.old_x, parent.old_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)
        self.color = (0, 127, 0)

    def move(self):
        self.old_x, self.old_y = self.x, self.y
        self.x, self.y = self.parent.old_x, self.parent.old_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)


class Snake(object):
    """The snake. Eat the food. Get Bigger. Don't die."""
    def __init__(self):
        self.head = Head()
        self.safe = Body(self.head)
        self.body = [Body(self.safe)]
        self.timer = 0
        self.food = Food()

    def update(self, time):
        self.timer += time
        if self.timer >= interval:
            self.head.move()
            self.safe.move()
            for s in self.body:
                s.move()
            if self.head.rect.colliderect(self.food.rect):
                self.body.append(Body(self.body[-1]))
                self.food = Food()
            if self.head.rect.collidelist([b.rect for b in self.body]) > -1 or\
               self.head.x < 0 or self.head.x > 29 or\
               self.head.y < 0 or self.head.y > 29:
                print("Game over, man.")
                pygame.quit()
                sys.exit()
            self.timer -= interval

        self.food.draw()
        self.head.draw()
        self.safe.draw()
        for s in self.body:
            s.draw()


class Food(object):
    """Thing to eat. Yum."""
    def __init__(self):
        self.x = randint(0, spaces - 1)
        self.y = randint(0, spaces - 1)
        spawn_y = self.y * square_size
        spawn_x = self.x * square_size
        self.rect = pygame.Rect(spawn_x, spawn_y, square_size, square_size)
        self.color = (0, 0, 200)

    def draw(self):
        pygame.draw.circle(display, self.color, self.rect.center, square_size/2)


pygame.init()
display = pygame.display.set_mode((square_size * spaces, square_size * spaces))
clock = pygame.time.Clock()
game = True
snake = Snake()

while game:
    time_elapsed = clock.tick()
    display.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN:
            if snake.head.vector_x == 0:
                if e.key == K_RIGHT or e.key == K_d:
                    snake.head.vector_x = 1
                    snake.head.vector_y = 0
                elif e.key == K_LEFT or e.key == K_a:
                    snake.head.vector_x = -1
                    snake.head.vector_y = 0
            elif snake.head.vector_y == 0:
                if e.key == K_UP or e.key == K_w:
                    snake.head.vector_y = -1
                    snake.head.vector_x = 0
                elif e.key == K_DOWN or e.key == K_s:
                    snake.head.vector_y = 1
                    snake.head.vector_x = 0
    snake.update(time_elapsed)
    pygame.display.update()