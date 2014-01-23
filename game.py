__author__ = 'Patrick'

import pygame
import sys
from pygame.locals import *
from random import randint, choice

interval = 150
square_size = 16
spaces = 30
fps = []
images = ["./images/redsquare.png", "./images/redcircle.png",
          "./images/bluesquare.png", "./images/bluecircle.png",
          "./images/greensquare.png", "./images/greencircle.png",
          "./images/yellowsquare.png", "./images/yellowcircle.png"]


class Segment(pygame.sprite.Sprite):
    """Parent class for Head and Body"""
    def __init__(self):
        super(Segment, self).__init__()
        self.rect = pygame.Rect(0, 0, square_size, square_size)
        self.old_x = -1
        self.old_y = 0
        self.color = (0, 0, 0)


class Head(Segment):
    """The snake's head. Collision detection!"""
    def __init__(self):
        super(Head, self).__init__()
        global square_size
        self.image = pygame.Surface((square_size, square_size))
        self.image.fill(0)
        self.image.set_colorkey(0)
        pygame.draw.circle(self.image, (0, 255, 0), (16/2, 16/2), 16 / 2)
        self.x, self.y = 0, 0
        self.vector_x = 1
        self.vector_y = 0
        self.color = (0, 255, 0)

    def update(self):
        self.old_x, self.old_y = self.x, self.y
        self.x += self.vector_x
        self.y += self.vector_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)


class Body(Segment):
    """The Snake's body. Don't bite yourself."""
    def __init__(self, parent, art):
        super(Body, self).__init__()
        global square_size
        self.image = art
        self.image.set_colorkey((255, 0, 181))
        self.parent = parent
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
        self.body = []
        self.timer = 0
        self.food = Food()
        self.add(self.food)

    def update(self, time):
        self.timer += time
        global interval
        if self.timer >= interval:
            super(Snake, self).update()
            self.timer -= interval
            for b in self.body:
                if b.x == self.head.x and b.y == self.head.y:
                    self.quit("Yow!\nGame over, man.")
            if self.food.x == self.head.x and self.food.y == self.head.y:
                try:
                    self.body.append(Body(self.body[-1], self.food.image))
                except IndexError:
                    self.body.append(Body(self.head, self.food.image))
                self.add(self.body[-1])
                self.remove(self.food)
                self.food = Food()
                self.add(self.food)
            if self.head.x < 0 or self.head.x > 29 or\
               self.head.y < 0 or self.head.y > 29:
                self.quit("Watch the walls!\nGame over, man.")

    @staticmethod
    def quit(message):
        print(message)
        print("FPS: %f" % ((sum(fps) / len(fps))))
        pygame.quit()
        sys.exit()


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
        self.image.set_colorkey((255, 0, 181))


pygame.init()
display = pygame.display.set_mode((square_size * spaces, square_size * spaces))
clock = pygame.time.Clock()
game = True
snake = Snake()

while game:
    time_elapsed = clock.tick()
    fps.append(clock.get_fps())
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