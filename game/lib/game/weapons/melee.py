import pygame
import math

from lib.game.weapons.weapon import Weapon


class Melee(Weapon):

    def __init__(self, x, y, horizontal, vertical, center_x, center_y, screen_size, damage):
        self.__angle = math.atan2(vertical - center_y - screen_size[1] / 2, horizontal - center_x - screen_size[0] / 2)
        self._vel_horizontal = math.cos(self.__angle) * 10
        self._vel_vertical = math.sin(self.__angle) * 10
        self._pos_x = x + 2 * self._vel_horizontal
        self._pos_y = y + 2 * self._vel_vertical
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/attack/cross.png'), (20, 20))
        self._time_of_life = 2
        self._collision_width = 50
        self._collision_height = 50
        self._damage = damage

