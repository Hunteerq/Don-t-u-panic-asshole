import json
import os
import pygame
from lib.game.world_objects.world_object import WorldObject

tree_sprite = [pygame.image.load('config/assets/objects/tree1.png'),
               pygame.image.load('config/assets/objects/tree2.png'),
               pygame.image.load('config/assets/objects/tree3.png'),
               pygame.image.load('config/assets/objects/tree4.png')]


object_config = None
file_exists = os.path.isfile("lib/config/objects/object_config.json")
if file_exists:
    with open("lib/config/objects/object_config.json") as json_file:
        object_config = json.load(json_file)


class Tree(WorldObject):

    def __init__(self, idx, sprite=0, x_coordinate=100, y_coordinate=100, width=70, height=70):
        super().__init__(idx, x_coordinate, y_coordinate, width, height, sprite)
        self._sprite_path = tree_sprite[self._rand_sprite]
        self._move_left_corner_x = 125
        self._move_left_corner_y = 125
        self._life = object_config['tree_hp']

        if self._rand_sprite == 0:
            self._move_left_corner_y = object_config['tree1_move_left_corner_y']
            self._move_left_corner_x = object_config['tree1_move_left_corner_x']
            self._width_collision = object_config['tree1_width_collision']
            self._height_collision = object_config['tree1_height_collision']

        elif self._rand_sprite == 1:
            self._move_left_corner_y = object_config['tree2_move_left_corner_y']
            self._move_left_corner_x = object_config['tree2_move_left_corner_x']
            self._width_collision = object_config['tree2_width_collision']
            self._height_collision = object_config['tree2_height_collision']

        elif self._rand_sprite == 2:
            self._move_left_corner_y = object_config['tree3_move_left_corner_y']
            self._move_left_corner_x = object_config['tree3_move_left_corner_x']
            self._width_collision = object_config['tree3_width_collision']
            self._height_collision = object_config['tree3_height_collision']

        elif self._rand_sprite == 3:
            self._move_left_corner_y = object_config['tree4_move_left_corner_y']
            self._move_left_corner_x = object_config['tree4_move_left_corner_x']
            self._width_collision = object_config['tree4_width_collision']
            self._height_collision = object_config['tree4_height_collision']
