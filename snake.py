__author__ = 'Patrick'

import pygame
from random import randint, choice
from pygame import transform
from pygame.locals import *
from config import *


class Body(pygame.sprite.Sprite):
    """Parent class for Head and Body"""
    def __init__(self, x, y, dictionary):
        super(Body, self).__init__()
        self.old_x = None
        self.old_y = None
        self.x = x
        self.y = y
        self.child = None
        self.image = dictionary["image"]
        self.rect = self.image.get_rect()
        self.color = dictionary["color"]
        self.type = dictionary["type"]
        self.rect.topleft = (self.x * square_size, self.y * square_size)

    def is_colliding_with(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def move(self, x, y):
        self.old_x, self.old_y = self.x, self.y
        self._move_child()
        self.x, self.y = x, y
        self.rect.topleft = (self.x * square_size, self.y * square_size)

    def _move_child(self):
        if self.child:
            self.child.move(self.old_x, self.old_y)


class Head(Body):
    def __init__(self, head_dict):
        super(Head, self).__init__(0, 0, head_dict)
        self.vector_x = 1
        self.vector_y = 0
        self.move_lock = False

    def update(self):
        self.old_x, self.old_y = self.x, self.y
        self._move_child()
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

    def rotate_left(self):
        self.image = transform.rotate(self.image, 90)

    def rotate_right(self):
        self.image = transform.rotate(self.image, -90)

    def control(self, key):
        if not self.move_lock:
            if self.vector_x in (-1, 1):
                if key in (K_w, K_UP):
                    self.vector_y = -1
                    self.rotate_left() if self.vector_x is 1 else self.rotate_right()
                if key in (K_s, K_DOWN):
                    self.vector_y = 1
                    self.rotate_right() if self.vector_x is 1 else self.rotate_left()
                if key in (K_w, K_s, K_UP, K_DOWN):
                    self.vector_x = 0
                    self.lock_toggle()
            elif self.vector_y in (-1, 1):
                if key in (K_d, K_RIGHT):
                    self.vector_x = 1
                    self.rotate_left() if self.vector_y is 1 else self.rotate_right()
                if key in (K_a, K_LEFT):
                    self.vector_x = -1
                    self.rotate_right() if self.vector_y is 1 else self.rotate_left()
                if key in (K_d, K_a, K_RIGHT, K_LEFT):
                    self.vector_y = 0
                    self.lock_toggle()


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
            tail = self._find_tail(self.head)
            tail.child = Body(tail.old_x, tail.old_y, choice(self.dictionary["candy"]))
            self.add(tail.child)

    def update(self, time):
        self.timer += time
        if self.timer >= interval:
            super(Snake, self).update()
            self.timer = 0
            # if self.head.is_colliding_with_body():
            #         self.quit("Yow!\nGame over, man.")
            for food in self.food_basket:
                if self.head.is_colliding_with(food):
                    if food.edible:
                        tail = self._find_tail(self.head)
                        tail.child = Body(tail.old_x, tail.old_y, food.dict)
                        self.add(tail.child)
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

    def quit(self, value):
        pygame.event.post(pygame.event.Event(25, message = value))

    def _find_tail(self, segment):
        if segment.child:
            return self._find_tail(segment.child)
        else:
            return segment