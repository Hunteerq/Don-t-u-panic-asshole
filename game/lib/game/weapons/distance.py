import pygame
import math
from lib.game.weapons.weapon import Weapon
from game.lib.game.weapons.weapon import Weapon
from game.lib.game.heroes.animations.bullet_animation import BulletAnimation


class Distance(Weapon):

    def __init__(self, x, y, horizontal, vertical, center_x, center_y, screen_size, damage):
        self.__angle = math.atan2(vertical - center_y - screen_size[1] / 2, horizontal - center_x - screen_size[0] / 2)
        self._vel_horizontal = math.cos(self.__angle) * 10
        self._vel_vertical = math.sin(self.__angle) * 10
        self._pos_x = x + self._vel_horizontal * 2
        self._pos_y = y + self._vel_vertical * 2
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/attack/bullet.png'), (30, 30))
        self._time_of_life = 100
        self._collision_width = 20
        self._collision_height = 20
        self._damage = damage
        self.__bullet_animation = BulletAnimation()

    def update_sprite(self):
        self._sprite = self.__bullet_animation.get_sprite()