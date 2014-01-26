__author__ = 'Patrick'

import pygame
import sys
from pygame.locals import *
from random import randint, choice

interval = 150
square_size = 16
half_square = square_size / 2
square_center = (half_square, half_square)
spaces = 20
images = ["./images/redsquare.png", "./images/redcircle.png",
          "./images/bluesquare.png", "./images/bluecircle.png",
          "./images/greensquare.png", "./images/greencircle.png",
          "./images/yellowsquare.png", "./images/yellowcircle.png"]
color_key = (255, 0, 181)


class Segment(pygame.sprite.Sprite):
    """Parent class for Head and Body"""
    def __init__(self):
        super(Segment, self).__init__()
        self.old_x = None
        self.old_y = None
        self.child = None
        self.parent = None

    def is_colliding_with(self, other):

        return (self.x, self.y) == (other.x, other.y)


class Head(Segment):
    """The snake's head. Collision detection!"""
    def __init__(self):
        super(Head, self).__init__()
        global square_size
        global half_square
        self.image = pygame.Surface((square_size, square_size))
        self.image.fill(0)
        self.image.set_colorkey(0)
        pygame.draw.circle(self.image, (0, 255, 0), square_center, half_square)
        self.x, self.y = 0, 0
        self.vector_x = 1
        self.vector_y = 0

    def update(self):
        self.old_x, self.old_y = self.x, self.y
        self.x += self.vector_x
        self.y += self.vector_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)

    def is_colliding_with_body(self):
        if self.child:
            return self._collision_helper(self.child)

    def _collision_helper(self, child):
        if child:
            return child.is_colliding_with(self) or self._collision_helper(child.child)
        else:
            return False


class Body(Segment):
    """The Snake's body. Don't bite yourself."""
    def __init__(self, parent, art):
        super(Body, self).__init__()
        global square_size
        self.image = art
        self.image.set_colorkey(color_key)
        self.parent = parent
        self.parent.child = self
        self.x, self.y = parent.old_x, parent.old_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)
        self.color = (0, 127, 0)

    def update(self):
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
        self.food = Food()
        self.add(self.food)

    def update(self, time):
        self.timer += time
        global interval
        if self.timer >= interval:
            super(Snake, self).update()
            self.timer -= interval
            if self.head.is_colliding_with_body():
                    self.quit("Yow!\nGame over, man.")
            if (self.food.x, self.food.y) == (self.head.x, self.head.y):
                self.add(Body(self._find_tail(self.head), self.food.image))
                self.remove(self.food)
                self.food = Food()
                self.add(self.food)
            if self.head.x < 0 or self.head.x > (spaces - 1) or\
               self.head.y < 0 or self.head.y > (spaces - 1):
                self.quit("Watch the walls!\nGame over, man.")

    @staticmethod
    def quit(message):
        print(message)
        pygame.quit()
        sys.exit()

    def _find_tail(self, segment):
        if segment.child:
            return self._find_tail(segment.child)
        else:
            return segment


class Food(pygame.sprite.Sprite):
    """Thing to eat. Yum."""
    def __init__(self):
        super(Food, self).__init__()
        self.x = randint(0, spaces - 1)
        self.y = randint(0, spaces - 1)
        spawn_y = self.y * square_size
        spawn_x = self.x * square_size
        self.rect = pygame.Rect(spawn_x, spawn_y, square_size, square_size)
        self.image = pygame.image.load(choice(images)).convert()
        self.image.set_colorkey(color_key)


pygame.init()
display = pygame.display.set_mode((square_size * spaces, square_size * spaces))
clock = pygame.time.Clock()
snake = Snake()

while True:
    time_elapsed = clock.tick()
    for e in pygame.event.get():
        if e.type == QUIT:
            Snake.quit("You quit!")
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
    display.fill(0)
    pygame.display.update(snake.draw(display))