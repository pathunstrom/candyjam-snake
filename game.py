__author__ = 'Patrick'

import pygame
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
snake_head_image = pygame.image.load('./images/jelly_green.png').convert()
snake_head_image = transform.rotate(snake_head_image, -90)
bad_food_image = {'image': pygame.image.load('./images/candyhumbug.png').convert(), 'type': 'bad', 'color': None}
image_lib = {'candy': candy_images, 'bad_food': bad_food_image, 'snake_head': snake_head_image}


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

    def _resolve(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.game_snake.Snake.quit("You quit!")
            elif e.type == KEYDOWN:
                if not self.game_snake.head.move_lock:
                    angle = 0
                    if self.game_snake.head.vector_x == 0:
                        if e.key == K_RIGHT or e.key == K_d:
                            self.game_snake.head.vector_x = 1
                            if self.game_snake.head.vector_y == 1:
                                angle = 90
                            elif self.game_snake.head.vector_y == -1:
                                angle = -90
                            self.game_snake.head.rotate(angle)
                            self.game_snake.head.vector_y = 0
                            self.game_snake.head.lock_toggle()
                        elif e.key == K_LEFT or e.key == K_a:
                            self.game_snake.head.vector_x = -1
                            if self.game_snake.head.vector_y == 1:
                                angle = -90
                            elif self.game_snake.head.vector_y == -1:
                                angle = 90
                            self.game_snake.head.rotate(angle)
                            self.game_snake.head.vector_y = 0
                            self.game_snake.head.lock_toggle()
                    elif self.game_snake.head.vector_y == 0:
                        if e.key == K_UP or e.key == K_w:
                            self.game_snake.head.vector_y = -1
                            if self.game_snake.head.vector_x == 1:
                                angle = 90
                            elif self.game_snake.head.vector_x == -1:
                                angle = -90
                            self.game_snake.head.vector_x = 0
                            self.game_snake.head.rotate(angle)
                            self.game_snake.head.lock_toggle()
                        elif e.key == K_DOWN or e.key == K_s:
                            self.game_snake.head.vector_y = 1
                            if self.game_snake.head.vector_x == 1:
                                angle = -90
                            elif self.game_snake.head.vector_x == -1:
                                angle = 90
                            self.game_snake.head.vector_x = 0
                            self.game_snake.head.rotate(angle)
                            self.game_snake.head.lock_toggle()


game = Game()

game.main_loop()