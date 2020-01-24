import json
import os
import pygame
from lib.game.world_objects.world_object import WorldObject

rock_sprite = [pygame.image.load('config/assets/objects/rock1.png'),
               pygame.image.load('config/assets/objects/rock2.png'),
               pygame.image.load('config/assets/objects/rock3.png'),
               pygame.image.load('config/assets/objects/rock4.png')]

object_config = None
file_exists = os.path.isfile("lib/config/objects/object_config.json")
if file_exists:
    with open("lib/config/objects/object_config.json") as json_file:
        object_config = json.load(json_file)


class Rock(WorldObject):

    def __init__(self, idx, sprite=0, x_coordinate=10, y_coordinate=10, width=70, height=70):
        super().__init__(idx, x_coordinate, y_coordinate, width, height, sprite)
        self._sprite_path = rock_sprite[self._rand_sprite]

        if self._rand_sprite == 0:
            self._move_left_corner_y = object_config['rock1_move_left_corner_y']
            self._move_left_corner_x = object_config['rock1_move_left_corner_x']
            self._width_collision = object_config['rock1_width_collision']
            self._height_collision = object_config['rock1_height_collision']

        elif self._rand_sprite == 1:
            self._move_left_corner_y = object_config['rock2_move_left_corner_y']
            self._move_left_corner_x = object_config['rock2_move_left_corner_x']
            self._width_collision = object_config['rock2_width_collision']
            self._height_collision = object_config['rock2_height_collision']

        elif self._rand_sprite == 2:
            self._move_left_corner_y = object_config['rock3_move_left_corner_y']
            self._move_left_corner_x = object_config['rock3_move_left_corner_x']
            self._width_collision = object_config['rock3_width_collision']
            self._height_collision = object_config['rock3_height_collision']

        elif self._rand_sprite == 3:
            self._move_left_corner_y = object_config['rock4_move_left_corner_y']
            self._move_left_corner_x = object_config['rock4_move_left_corner_x']
            self._width_collision = object_config['rock4_width_collision']
            self._height_collision = object_config['rock4_height_collision']
