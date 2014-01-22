__author__ = 'Patrick'

import pygame
import sys
from pygame.locals import *
from random import randint, choice


interval = 150
square_size = 16
square_tuple = (square_size, square_size)
spaces = 30
images = ["images/redsquare.png", "images/redcirlce.png",
          "images/bluesquare.png", "images/bluecircle.png",
          "images/greensquare.png", "images/greencircle.png",
          "images/yellowsquare.png", "images/yellowcircle.png"]


class Segment(pygame.sprite.Sprite):
    """Parent class for Head and Body"""
    def __init__(self):
        super(Segment, self).__init__()
        self.rect = pygame.Rect((0, 0), square_tuple)
        self.old_x = -1
        self.old_y = 0
        self.color = (0, 0, 0)

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect)

    def move(self):
        pass

    def update(self):
        self.move()


class Head(Segment):
    """The snake's head. Collision detection!"""
    def __init__(self):
        super(Head, self).__init__()
        self.image = pygame.Surface(square_tuple)
        self.image.fill(000)
        self.image.set_colorkey(000)
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


class Snake(pygame.sprite.OrderedUpdates):
    """The snake. Eat the food. Get Bigger. Don't die."""
    def __init__(self):
        super(Snake, self).__init__()
        self.head = Head()
        self.add(self.head)
        self.timer = 0

class Food(pygame.sprite.Sprite):
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
    snake.update()
    snake.draw(display)
    pygame.display.update()