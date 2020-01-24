import pygame
from math import fabs
import glob

attack_right = glob.glob('config/assets/attack/close/right/*.png')
attack_left = glob.glob('config/assets/attack/close/left/*.png')
attack_up = glob.glob('config/assets/attack/close/up/*.png')
attack_down = glob.glob('config/assets/attack/close/down/*.png')

SPRITE_AMOUNT = 4
SPRITE_CHANGE_DELTA_TIME = 100


class MainHeroAttack:

    __move_count = 0
    __last_update_time = 0
    __sprite_count = 0
    __direction = ''

    @staticmethod
    def get_sprite(self):

        if self.__direction == 'left':
            sprite = attack_left[self.__sprite_count]
        elif self.__direction == 'right':
            sprite = attack_right[self.__sprite_count]
        elif self.__direction == 'up':
            sprite = attack_up[self.__sprite_count]
        else:
            sprite = attack_down[self.__sprite_count]

        return sprite

    @staticmethod
    def attack_animation(self):
        actual_time = pygame.time.get_ticks()

        if fabs(actual_time - self.__last_update_time) >= SPRITE_CHANGE_DELTA_TIME:
            self.__sprite_count += 1
            self.__last_update_time = actual_time

        if self.__sprite_count == SPRITE_AMOUNT:
            self.__sprite_count = 0
            return False

        return pygame.image.load(self.get_sprite(MainHeroAttack))

    def set_direction(self, direction):
        self.__direction = direction
