import pygame
import os
import json
import glob
from math import fabs
from lib.game.equipment_and_crafting.equipment import Equipment

main_hero_config = None
main_hero_config_dir = "lib/config/heroes/main_hero_config.json"
file_exists = os.path.isfile(main_hero_config_dir)
if file_exists:
    with open(main_hero_config_dir) as json_file:
        main_hero_config = json.load(json_file)
BASE_SPEED = main_hero_config['baseSpeed'] if main_hero_config is not None else 300
HEIGHT = main_hero_config['height'] if main_hero_config is not None else 40
WIDTH = main_hero_config['width'] if main_hero_config is not None else 35
CENTER_X = main_hero_config['center_x'] if main_hero_config is not None else 20
CENTER_Y = main_hero_config['center_y'] if main_hero_config is not None else 20
SPRITE_AMOUNT_VERTICAL = 3
SPRITE_AMOUNT_HORIZONTAL = 5
SPRITE_CHANGE_DELTA_TIME = 100

IDLE_SPEED = 0

right_sprite = glob.glob('config/assets/movement/right/*.png')
down_sprite = glob.glob('config/assets/movement/down/*.png')
left_sprite = glob.glob('config/assets/movement/left/*.png')
up_sprite = glob.glob('config/assets/movement/up/*.png')


class MainHero:
    __movement_left = False
    __movement_right = False
    __movement_up = False
    __movement_down = False
    __move_count = 0
    __last_update_time = 0
    __hit_points = 100
    __nick = ''

    def __init__(self, game_runner, game, position, nickname, hp, items: []):
        self.__character = pygame.image.load('config/assets/movement/main_hero.png')
        self.__move_speed = BASE_SPEED
        self.__position_x = position[0]
        self.__position_y = position[1]
        self._height = HEIGHT
        self._width = WIDTH
        self.__game = game
        self.__game_runner = game_runner
        self.__udp_connector = self.__game.get_udp_connector()
        self.__objects = game_runner.get_objects()
        self.__delta_time = 0
        self.__flag = False
        self.__col_flag = False
        self.__center_x = CENTER_X  # hero isn't exactly at center screen
        self.__center_y = CENTER_Y
        self.__standing = "right"
        self.__equipment = Equipment()
        self.__hit_points = hp
        self.__nick = nickname
        for item in items:
            self.__equipment.pick_up_item(item)
        self.__screen = self.__game.get_screen()
        self.__screen_size = self.__screen.get_size()
        self.__damage = main_hero_config['fist_damage']
        self.__horizontal_speed = IDLE_SPEED
        self.__vertical_speed = IDLE_SPEED

    def get_character(self):
        return self.__character

    def get_nick(self):
        return self.__nick

    def get_move_speed(self):
        return self.__move_speed

    def update_position(self, horizontal_speed, vertical_speed):
        self.__col_flag = False
        self.__objects = self.__game_runner.get_objects()
        # horizontal check
        self.__position_x += horizontal_speed

        for world_object in self.__objects:
            if world_object.check_collision(self.__position_x - self.__screen_size[0] / 2,
                                            self.__position_y - self.__screen_size[1] / 2, self._width,
                                            self._height, self.__center_x, self.__center_y):
                self.__col_flag = True
                if horizontal_speed > 0:
                    # Hero]->[]
                    self.__position_x = world_object.get_x() + world_object.get_mv_x() - self._width \
                                        - self.__center_x
                else:
                    # [] <-[Hero
                    self.__position_x = world_object.get_x() + world_object.get_width_collision() \
                                        + world_object.get_mv_x() - self.__center_x

        # vertical check
        self.__position_y += vertical_speed
        for world_object in self.__objects:
            if world_object.check_collision(self.__position_x - self.__screen_size[0] / 2,
                                            self.__position_y - self.__screen_size[1] / 2, self._width,
                                            self._height, self.__center_x, self.__center_y):
                self.__col_flag = True
                if vertical_speed > 0:
                    #  \/ Hero Down
                    #  []
                    self.__position_y = world_object.get_y() + world_object.get_mv_y() - self._height \
                                        - self.__center_y
                else:
                    #  []
                    #  /\ Hero Up
                    self.__position_y = world_object.get_y() + world_object.get_height_collision() \
                                        + world_object.get_mv_y() - self.__center_y

    def get_sprite(self):
        self.update_sprite()

        if self.__movement_left:
            sprite = left_sprite[self.__move_count % SPRITE_AMOUNT_HORIZONTAL]
        elif self.__movement_right:
            sprite = right_sprite[self.__move_count % SPRITE_AMOUNT_HORIZONTAL]
        elif self.__movement_up:
            sprite = up_sprite[self.__move_count % SPRITE_AMOUNT_VERTICAL]
        elif self.__movement_down:
            sprite = down_sprite[self.__move_count % SPRITE_AMOUNT_VERTICAL]
        else:
            sprite = self.get_standing_sprite()

        return pygame.image.load(sprite)

    def update_sprite(self):
        actual_time = pygame.time.get_ticks()
        if fabs(actual_time - self.__last_update_time) >= SPRITE_CHANGE_DELTA_TIME:
            self.__move_count += 1
            self.__last_update_time = actual_time

    def reset_direction(self, direction):
        if direction == pygame.K_d:
            self.__movement_right = False
            self.__standing = "right"
        if direction == pygame.K_a:
            self.__movement_left = False
            self.__standing = "left"
        if direction == pygame.K_s:
            self.__movement_down = False
            self.__standing = "down"
        if direction == pygame.K_w:
            self.__movement_up = False
            self.__standing = "up"
        self.__move_count = 0

    def set_movement_right(self):
        self.__movement_left = False
        self.__movement_right = True

    def set_movement_left(self):
        self.__movement_right = False
        self.__movement_left = True

    def set_movement_up(self):
        self.__movement_up = True
        self.__movement_down = False

    def set_movement_down(self):
        self.__movement_down = True
        self.__movement_up = False

    def set_horizontal_speed(self, speed):
        self.__horizontal_speed = speed

    def set_vertical_speed(self, speed):
        self.__vertical_speed = speed

    def get_damage(self):
        return self.__damage

    def get_standing_sprite(self):
        if self.__standing == "left":
            return left_sprite[0]
        if self.__standing == "right":
            return right_sprite[0]
        if self.__standing == "up":
            return up_sprite[0]
        if self.__standing == "down":
            return down_sprite[0]

    def get_x(self):
        return self.__position_x

    def get_y(self):
        return self.__position_y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_col_flag(self):
        return self.__col_flag

    def get_center_x(self):
        return self.__center_x

    def get_center_y(self):
        return self.__center_y

    def get_equipment(self):
        return self.__equipment

    def get_horizontal_speed(self):
        return self.__horizontal_speed

    def get_vertical_speed(self):
        return self.__vertical_speed

    def get_damage(self):
        return self.__damage
