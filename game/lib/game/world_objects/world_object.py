import pygame
from random import randint


class WorldObject:

    _x_coordinate = None
    _y_coordinate = None
    _height = None
    _width = None
    _sprite_path = None
    _move_left_corner_x = None
    _move_left_corner_y = None
    _width_collision = None
    _height_collision = None
    _object_id = None
    _life = None

    def __init__(self,  idx, x_coordinate, y_coordinate, width, height, sprite=0):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._width = width
        self._height = height
        self._width_collision = width
        self._height_collision = height
        self._move_left_corner_x = 0
        self._move_left_corner_y = 0
        self._rand_sprite = sprite
        self._object_id = idx

    def get_id(self):
        return self._object_id

    def get_x(self):
        return self._x_coordinate

    def get_y(self):
        return self._y_coordinate

    def get_mv_x(self):
        return self._move_left_corner_x

    def get_mv_y(self):
        return self._move_left_corner_y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_width_collision(self):
        return self._width_collision

    def get_height_collision(self):
        return self._height_collision

    def get_sprite(self):
        return self._sprite_path

    def set_x(self, value):
        self._x_coordinate = value

    def set_y(self, value):
        self._y_coordinate = value

    def change_position_on_screen(self):
        actual_time = pygame.time.get_ticks()

    def __handle_vertical_collision(self, y_object, moving_object_y, moving_object_height):
        if y_object + self._move_left_corner_y < moving_object_y \
                < y_object + self._move_left_corner_y + self._height_collision:
            return True
        elif y_object + self._move_left_corner_y < (moving_object_y + moving_object_height) \
                < (y_object + self._move_left_corner_y + self._height_collision):
            return True
        else:
            return False


    def __handle_horizontal_collision(self, x_object, moving_object_x, moving_object_width):
        if x_object + self._move_left_corner_x < moving_object_x < (x_object + self._move_left_corner_x
                                                                    + self._width_collision) \
                or x_object + self._move_left_corner_x < (moving_object_x + moving_object_width) \
                < (x_object + self._width_collision + self._move_left_corner_x):
            return True
        else:
            return False

    def check_collision(self, hero_pos_x, hero_pos_y, hero_width, hero_height, center_x, center_y):
        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        x_object, y_object = self._x_coordinate - hero_pos_x, self._y_coordinate - hero_pos_y
        hero_x, hero_y = width / 2 + center_x, height / 2 + center_y
        if self.__handle_horizontal_collision(x_object, hero_x, hero_width):
            if self.__handle_vertical_collision(y_object, hero_y, hero_height):
                return True
            else:
                return False
        else:
            return False

    def draw_collision_rect(self, screen, hero_pos_x, hero_pos_y, hero_width, hero_height, center_x, center_y):
        x_object, y_object = self._x_coordinate - hero_pos_x, self._y_coordinate - hero_pos_y
        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        hero_x, hero_y = width / 2 + center_x, height / 2 + center_y
        pygame.draw.rect(screen, (255, 0, 255), [x_object + self._move_left_corner_x, y_object
                                                 + self._move_left_corner_y,self._width_collision,
                                                 self._height_collision], 1)
        pygame.draw.rect(screen, (255, 0, 0), [hero_x, hero_y, hero_width, hero_height], 1)


    def check_collision_weapon(self, weapon_x, weapon_y, weapon_width, weapon_height):
        width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
        x_object, y_object = self._x_coordinate + width / 2, self._y_coordinate + height / 2

        if self.__handle_horizontal_collision(x_object, weapon_x, weapon_width):
            if self.__handle_vertical_collision(y_object, weapon_y, weapon_height):
                return True
            else:
                return False
        else:
            return False

    def get_life(self):
        return self._life


    def update_life(self, damage):
        self._life -= damage
