import pygame
from math import fabs
import glob

bullet = glob.glob('config/assets/attack/distant/*.png')

SPRITE_AMOUNT = 71
SPRITE_CHANGE_DELTA_TIME = 100


class BulletAnimation:

    def __init__(self):
        self.__last_update_time = 0
        self.__sprite_count = 0

    def get_sprite(self):
        actual_time = pygame.time.get_ticks()
        if fabs(actual_time - self.__last_update_time) >= SPRITE_CHANGE_DELTA_TIME:
            self.__sprite_count += 1
            self.__last_update_time = actual_time

        if self.__sprite_count == SPRITE_AMOUNT:
            self.__sprite_count = 0

        return pygame.transform.scale(pygame.image.load(bullet[self.__sprite_count]), (40, 40))

    def reset_sprite(self):
        self.__sprite_count = 0
        self.__last_update_time = 0
