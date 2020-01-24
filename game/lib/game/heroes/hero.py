import pygame
import glob
from lib.game.world_objects.world_object import WorldObject

right_sprite = glob.glob('config/assets/movement/right/*.png')
down_sprite = glob.glob('config/assets/movement/down/*.png')
left_sprite = glob.glob('config/assets/movement/left/*.png')
up_sprite = glob.glob('config/assets/movement/up/*.png')


class Hero(WorldObject):

    def __init__(self, x_coordinate, y_coordinate, hp, nick, items, id, width=40, height=40):
        super().__init__(id, x_coordinate, y_coordinate, width, height)
        self._sprite_path = pygame.image.load('config/assets/movement/main_hero.png')
        self.__hp = 2
        self.__nick = 'elo'
        self.__items = []

