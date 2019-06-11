import pygame
from lib.game.heroes.main_hero import MainHero
from lib.game.map import Map
from lib.game.object_generator import ObjectGenerator
from lib.connections.request import request_types
from lib.game.heroes.hero import Hero
from lib.config.controllers.controller import Controller
from lib.game.heroes.hero_movement import HeroMovement
from lib import gamestates
from lib.game.world_objects.rock import Rock
from lib.game.world_objects.tree import Tree


IDLE_SPEED = 0
CROSS_SPEED = 0.7071


class GameRunner:

    def __init__(self, game_object):
        self.__game = game_object
        self.__main_hero_pos = tuple(map(lambda x: x / 2, self.__game.get_screen().get_size()))
        self.__screen = self.__game.get_screen()
        self.__screen_size = self.__screen.get_size()
        self.__map = Map(self.__game)
        self.__udp_connector = self.__game.get_udp_connector()
        self.__objects = []
        self.__main_hero = None
        self.__main_hero_horizontal_speed = IDLE_SPEED
        self.__main_hero_vertical_speed = IDLE_SPEED
        self.__eq_slot_sprite = None
        self.__eq_slot_width = 64
        self.__marked_slot_sprite = None
        self.__1_key_value = 49
        self.__lower_margin = 84
        self.__shift_from_middle = 160
        self.__x_index = 0
        self.__y_index = 1
        self.__hero_data = None
        self.__movement_events = []

    def __create_hero(self, hero_data):
        if self.__main_hero is None:
            hp = hero_data['health']
            items = hero_data['items']
            nickname = hero_data['nick']
            position = hero_data['position']
            self.__main_hero = MainHero(self, self.__game, position, nickname, hp, items)
            self.__game.pass_hero(self.__main_hero)
            self.__eq_slot_sprite = self.__main_hero.get_equipment().get_background()
            self.__marked_slot_sprite = self.__main_hero.get_equipment().get_marked_background()

    def loop(self):
        self.__game.create_udp_connection_thread()
        self.__check_server_response()
        if self.__main_hero is not None:
            self.__handle_events()
            self.__transform()
            self.__draw()

    def __handle_events(self):
        for event in self.__game.get_events():
            self.__handle_keydown_events(event)
            self.__handle_keyup_events(event)
            self.__handle_number_key_event(event)

    def __handle_keydown_events(self, event):
        if event.type == pygame.KEYDOWN and self.__check_event_type(event) == 'movement':
            self.__movement_events.append(event.key)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.__game.set_state(gamestates.GAME_MENU)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            HeroMovement.movement_up(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            HeroMovement.movement_down(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            HeroMovement.movement_left(self.__main_hero, self.__game)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            HeroMovement.movement_right(self.__main_hero, self.__game)

        if self.__movement_events.count(Controller.D.value) > 0 \
                and self.__movement_events.count(Controller.W.value) > 0:
            HeroMovement.movement_up_right(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.S.value) > 0 \
                and self.__movement_events.count(Controller.D.value) > 0:
            HeroMovement.movement_down_right(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.A.value) > 0 \
                and self.__movement_events.count(Controller.S.value) > 0:
            HeroMovement.movement_down_left(self.__main_hero, self.__game)
        elif self.__movement_events.count(Controller.A.value) > 0 \
                and self.__movement_events.count(Controller.W.value) > 0:
            HeroMovement.movement_up_left(self.__main_hero, self.__game)

    def __handle_keyup_events(self, event):
        if event.type == pygame.KEYUP and self.__check_event_type(event) == 'movement':
            self.__movement_events.remove(event.key)
        if event.type == pygame.KEYUP and (event.key == pygame.K_w or event.key == pygame.K_s):
            self.__main_hero.set_vertical_speed(IDLE_SPEED)
            self.__main_hero.reset_direction(event.key)
        elif event.type == pygame.KEYUP and (event.key == pygame.K_a or event.key == pygame.K_d):
            self.__main_hero.set_horizontal_speed(IDLE_SPEED)
            self.__main_hero.reset_direction(event.key)
        if self.__movement_events.count(Controller.W.value) > 0:
            self.__main_hero.set_vertical_speed(-HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.S.value) > 0:
            self.__main_hero.set_vertical_speed(HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.A.value) > 0:
            self.__main_hero.set_horizontal_speed(-HeroMovement.hero_move_converter(self.__main_hero, self.__game))
        elif self.__movement_events.count(Controller.D.value) > 0:
            self.__main_hero.set_horizontal_speed(HeroMovement.hero_move_converter(self.__main_hero, self.__game))

    def __hero_move_converter(self, hero):
        return hero.get_move_speed() * self.__game.get_delta_time()

    def __handle_number_key_event(self, event):
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_2 or
                                             event.key == pygame.K_3 or event.key == pygame.K_4 or
                                             event.key == pygame.K_5):
            value = event.key - self.__1_key_value
            self.__main_hero.get_equipment().mark_item(value)

    def __transform(self):
        if not self.__main_hero.get_col_flag():
            self.__map.change_bias_x(self.__main_hero.get_horizontal_speed())
            self.__map.change_bias_y(self.__main_hero.get_vertical_speed())
        self.__main_hero.update_position(self.__main_hero.get_horizontal_speed(), self.__main_hero.get_vertical_speed())

    def __draw(self):
        self.__map.fill_screen_with_grass()
        self.__screen.blit(self.__main_hero.get_sprite(), self.__main_hero_pos)
        for world_object in self.__objects:
            self.__screen.blit(world_object.get_sprite(),
                               (
                               world_object.get_x() - self.__main_hero.get_x() + self.__screen_size[self.__x_index] / 2,
                               world_object.get_y() - self.__main_hero.get_y()
                               + self.__screen_size[self.__y_index] / 2))
        marked_index = self.__main_hero.get_equipment().get_marked_index()
        for y in range(0, 5):
            if y == marked_index:
                self.__screen.blit(self.__marked_slot_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))

            else:
                self.__screen.blit(self.__eq_slot_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))
            if self.__main_hero.get_equipment().get_item_by_index(y) is not None:
                item_sprite = self.__main_hero.get_equipment()
                item_sprite = item_sprite.get_item_by_index(y)
                item_sprite = item_sprite.get_sprite()
                self.__screen.blit(item_sprite,
                                   ((self.__screen_size[self.__x_index] / 2) + y * self.__eq_slot_width
                                    - self.__shift_from_middle,
                                    self.__screen_size[self.__y_index] - self.__lower_margin))

    def get_objects(self):
        return self.__objects

    def __check_server_response(self):
        server_responses = self.__game.get_udp_server_responses()
        for response in server_responses:
            if response['type'] == request_types.UDP_LOGIN:
                if self.__main_hero is None:
                    self.__create_hero(response['data'][0])
                    self.__create_objects(response['data'][1:])
            elif response['type'] == request_types.UDP_SERVER_UPDATE:
                self.__create_objects(response['data'])
            elif response['type'] == request_types.UDP_UPDATE_POSITION:
                self.update_positions(response)
                self.__objects.sort(key=lambda y_coord: y_coord.get_y())

    def update_positions(self, response):
        object_data = response['data']
        for world_object in self.__objects:
            if world_object.get_id() == object_data['idx']:
                position = object_data['position']['py/tuple']
                world_object.set_x(position[0])
                world_object.set_y(position[1])

    def __create_objects(self, object_list):
        self.__objects = []
        for world_object in object_list:
            if 'object_type' in world_object:
                if world_object['py/object'] == 'lib.model.character.Character' and \
                        world_object['nick'] != self.__main_hero.get_nick():
                    hp = world_object['health']
                    nick = world_object['nick']
                    items = world_object['items']
                    object_id = world_object['idx']
                    position = world_object['position']['py/tuple']
                    self.__objects.append(Hero(position[0], position[1], hp, nick, items, object_id))
                elif world_object['object_type'] == 2 or world_object['object_type'] == 4:
                    position = world_object['position']['py/tuple']
                    object_id = world_object['idx']
                    sprite = world_object['sprite']
                    self.__objects.append(Rock(sprite, object_id, position[0], position[1]))
                elif world_object['object_type'] == 6:
                    position = world_object['position']['py/tuple']
                    object_id = world_object['idx']
                    sprite = world_object['sprite']
                    self.__objects.append(Tree(sprite, object_id, position[0], position[1]))
        self.__objects.sort(key=lambda y_coord: y_coord.get_y())

    def __check_event_type(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
            return 'movement'
