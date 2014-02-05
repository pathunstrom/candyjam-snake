__author__ = 'Patrick'

import pygame
import sys
from pygame.locals import *
from pygame import transform
import snake
from config import *


pygame.init()
display = pygame.display.set_mode((square_size * spaces, square_size * spaces))

candy_images = [{'image': pygame.image.load('./images/bean_purple.png').convert(), 'type': bean, 'color': purple},
                {'image': pygame.image.load('./images/bean_orange.png').convert(), 'type': bean, 'color': orange},
                {'image': pygame.image.load('./images/bean_green.png').convert(), 'type': bean, 'color': green},
                {'image': pygame.image.load('./images/bean_wild.png').convert(), 'type': bean, 'color': wild},
                {'image': pygame.image.load('./images/lollipop_purple.png').convert(), 'type': lollipop, 'color': purple},
                {'image': pygame.image.load('./images/lollipop_orange.png').convert(), 'type': lollipop, 'color': orange},
                {'image': pygame.image.load('./images/lollipop_green.png').convert(), 'type': lollipop, 'color': green},
                {'image': pygame.image.load('./images/lollipop_wild.png').convert(), 'type': lollipop, 'color': wild},
                {'image': pygame.image.load('./images/mm_purple.png').convert(), 'type': mm, 'color': purple},
                {'image': pygame.image.load('./images/mm_orange.png').convert(), 'type': mm, 'color': orange},
                {'image': pygame.image.load('./images/mm_green.png').convert(), 'type': mm, 'color': green},
                {'image': pygame.image.load('./images/mm_wild.png').convert(), 'type': mm, 'color': wild},
                {'image': pygame.image.load('./images/star_purple.png').convert(), 'type': star, 'color': purple},
                {'image': pygame.image.load('./images/star_orange.png').convert(), 'type': star, 'color': orange},
                {'image': pygame.image.load('./images/star_green.png').convert(), 'type': star, 'color': green},
                {'image': pygame.image.load('./images/star_wild.png').convert(), 'type': star, 'color': wild},
                {'image': pygame.image.load('./images/swirl_purple.png').convert(), 'type': swirl, 'color': purple},
                {'image': pygame.image.load('./images/swirl_orange.png').convert(), 'type': swirl, 'color': orange},
                {'image': pygame.image.load('./images/swirl_green.png').convert(), 'type': swirl, 'color': green},
                {'image': pygame.image.load('./images/swirl_wild.png').convert(), 'type': swirl, 'color': wild}]
snake_head_image = {'image': pygame.image.load('./images/jelly_green.png').convert(), 'type': 'head', 'color': None}
snake_head_image["image"] = transform.rotate(snake_head_image["image"], -90)
bad_food_image = {'image': pygame.image.load('./images/candyhumbug.png').convert(), 'type': 'bad', 'color': None}
image_lib = {'candy': candy_images, 'bad_food': bad_food_image, 'snake_head': snake_head_image}

MOVE_KEYS = [K_w, K_a, K_s, K_d, K_RIGHT, K_LEFT, K_UP, K_DOWN]

class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_snake = snake.Snake(image_lib)

    def main_loop(self):
        while True:
            time_elapsed = self.clock.tick()
            self._resolve()
            self.game_snake.update(time_elapsed)
            display.fill((0, 0, 0))
            pygame.display.update(self.game_snake.draw(display))

    def pause_loop(self):
        while True:
            if pygame.event.peek(KEYUP):
                events = pygame.event.get(KEYUP)
                event = events.pop()
                if event.key == K_ESCAPE:
                    pygame.event.clear()
                    break
            if pygame.event.peek(QUIT):
                self.quit("Quit from pause")

    def quit(self, message):
        print(message)
        pygame.quit()
        sys.exit()

    def _resolve(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.quit("You quit!")
            elif e.type == COLLIDE:
                self.quit(e.message)
            elif e.type == KEYUP and e.key == K_ESCAPE:
                self.pause_loop()
            elif e.type == KEYDOWN:
                if e.key in MOVE_KEYS:
                    self.game_snake.head.control(e.key)


game = Game()
game.main_loop()