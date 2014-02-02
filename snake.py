__author__ = 'Patrick'

import pygame
import sys
from random import randint, choice
from pygame import transform
from config import *


class Segment(pygame.sprite.Sprite):
    """Parent class for Head and Body"""
    def __init__(self):
        super(Segment, self).__init__()
        self.old_x = None
        self.old_y = None
        self.child = None
        self.parent = None  # Remove
        self.image = pygame.Surface(square)
        self.rect = self.image.get_rect()

    def is_colliding_with(self, other):
        return (self.x, self.y) == (other.x, other.y)


class Head(Segment):
    def __init__(self, head_image):
        super(Head, self).__init__()
        self.image = head_image
        self.rect = self.image.get_rect()
        self.x, self.y = 0, 0
        self.vector_x = 1
        self.vector_y = 0
        self.move_lock = False

    def update(self):
        self.old_x, self.old_y = self.x, self.y
        self.x += self.vector_x
        self.y += self.vector_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)
        if self.move_lock:
            self.lock_toggle()

    def is_colliding_with_body(self):
        if self.child:
            return self._collision_helper(self.child)

    def _collision_helper(self, child):
        if child:
            return child.is_colliding_with(self) or self._collision_helper(child.child)
        else:
            return False

    def lock_toggle(self):
        self.move_lock = not self.move_lock

    def rotate(self, rotation):
        self.image = transform.rotate(self.image, rotation)


class Body(Segment):
    """The Snake's body. Don't bite yourself."""
    def __init__(self, parent, dictionary):
        super(Body, self).__init__()
        self.image = dictionary['image']
        self.type = dictionary['type']
        self.color = dictionary['color']
        self.rect = self.image.get_rect()
        self.parent = parent
        self.parent.child = self
        self.x, self.y = parent.old_x, parent.old_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)

    def update(self):
        self.old_x, self.old_y = self.x, self.y
        self.x, self.y = self.parent.old_x, self.parent.old_y
        self.rect.topleft = (self.x * square_size, self.y * square_size)


class Food(pygame.sprite.Sprite):
    """Thing to eat. Yum."""
    def __init__(self, head, definition):
        super(Food, self).__init__()
        self.head = head
        self.x = randint(1, spaces - 2)
        self.y = randint(1, spaces - 2)
        before_head_x = (self.head.x + self.head.vector_x)
        before_head_y = (self.head.y + self.head.vector_y)
        before_head = (before_head_x, before_head_y)
        while self._collide(self.head) or (self.x, self.y) == before_head:
            self.x = randint(1, spaces - 2)
            self.y = randint(1, spaces - 2)
        self.edible = False
        spawn_y = self.y * square_size
        spawn_x = self.x * square_size
        self.rect = pygame.Rect(spawn_x, spawn_y, square_size, square_size)
        self.image = definition['image']
        self.dict = definition

    def is_surrounded(self):
        current_position = (self.x, self.y)
        self.x += 1
        value = False
        if self._collide(self.head):
            self.x = current_position[0]
            self.x -= 1
            if self._collide(self.head):
                self.x = current_position[0]
                self.y += 1
                if self._collide(self.head):
                    self.y = current_position[1]
                    self.y -= 1
                    if self._collide(self.head):
                        value = True
        self.x, self.y = current_position
        return value

    def _collide(self, segment):
        if segment.child:
            return segment.is_colliding_with(self) or self._collide(segment.child)
        else:
            return segment.is_colliding_with(self)



class Snake(pygame.sprite.OrderedUpdates):
    """The snake. Eat the food. Get Bigger. Don't die."""
    def __init__(self, lib):
        super(Snake, self).__init__()
        self.dictionary = lib
        self.timer = 0
        self.head = Head(self.dictionary['snake_head'])
        self.add(self.head)
        self.food_basket = [Food(self.head, self.dictionary['bad_food'])]
        self.add(self.food_basket[0])
        for x in range(6):
            self.update(interval)
            self.add(Body(self._find_tail(self.head), choice(self.dictionary['candy'])))

    def update(self, time):
        self.timer += time
        if self.timer >= interval:
            super(Snake, self).update()
            self.timer = 0
            if self.head.is_colliding_with_body():
                    self.quit("Yow!\nGame over, man.")
            for food in self.food_basket:
                if self.head.is_colliding_with(food):
                    if food.edible:
                        self.add(Body(self._find_tail(self.head), food.dict))
                        self.remove(food)
                        self.food_basket.remove(food)
                    else:
                        self.quit("Bad food.\nGame over, man.")
                if food.is_surrounded() and not food.edible:
                    self.food_basket.append(Food(self.head, self.dictionary['bad_food']))
                    self.add(self.food_basket[-1])
                    food.edible = True
                    food.dict = choice(self.dictionary['candy'])
                    food.image = food.dict['image']
            if self.head.x < 0 or self.head.x > (spaces - 1) or\
               self.head.y < 0 or self.head.y > (spaces - 1):
                self.quit("Watch the walls!\nGame over, man.")

    @staticmethod
    def quit(message):
        # pygame.image.save(display, './gamescreenshot.png')
        print(message)
        pygame.quit()
        sys.exit()

    def _find_tail(self, segment):
        if segment.child:
            return self._find_tail(segment.child)
        else:
            return segment

    def count_body(self, segment):
        if segment.child:
            return 1 + self.count_body(segment.child)
        else:
            return 1