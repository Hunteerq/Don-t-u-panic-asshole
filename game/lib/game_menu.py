import pygame
import pygame.freetype
import json
import os
from lib import colors
from lib import gamestates
from lib import button

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
FONT_SIZE_TITLE = game_config['menu_title_font_size'] if game_config is not None else 70
FONT_SIZE_MENU = game_config['menu_font_size'] if game_config is not None else 50


class GameMenu:

    def __init__(self, game):
        self.__game = game
        self.__screen_size = self.__game.get_screen().get_size()
        self.__text_menu_height = FONT_SIZE_MENU
        self.__text_title_height = FONT_SIZE_TITLE
        self.__text_menu_font = pygame.freetype.SysFont(FONT_STYLE, self.__text_menu_height)
        self.__font_game_title = pygame.freetype.SysFont(FONT_STYLE, self.__text_title_height)
        self.__empty_rect = 2
        self.__width_size = 0
        self.__height_size = 1
        self.__title_pos_y = self.__screen_size[self.__height_size] / 9
        self.__title_pos_x = self.__screen_size[self.__width_size] / 16
        self.__new_line_title = self.__text_title_height + self.__text_title_height / 3
        self.__new_line = self.__text_menu_height + self.__text_menu_height / 2
        self.__button_pos_x = self.__screen_size[self.__width_size] / 16
        self.__button_pos_y = self.__screen_size[self.__height_size] / 9 + self.__title_pos_y + 2 * self.__new_line_title
        self.__button_start = button.Button(self.__button_pos_x, self.__button_pos_y, 0.2, 0.1, text='Continue',
                                            function=self.choice, args="Continue")
        self.__button_controls = button.Button(self.__button_pos_x, self.__button_pos_y + 1 * self.__new_line, 0.2, 0.1,
                                                text='Controls', function=self.choice, args="Controls")
        self.__button_exit = button.Button(self.__button_pos_x, self.__button_pos_y + 2 * self.__new_line, 0.2, 0.1,
                                           text='Exit', function=self.choice, args="Exit")
        print("Game Menu initialized")

    def choice(self, text):
        self.__game.set_last_state(gamestates.GAME_MENU)
        if text == 'Continue':
            self.__game.set_state(gamestates.GAME)
        elif text == 'Controls':
            self.__game.set_state(gamestates.CONTROLS)
        elif text == 'Exit':
            self.__game.set_state(gamestates.QUIT)

    def loop(self):
        events = self.__game.get_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__game.set_state(gamestates.GAME)
                return

        self.__font_game_title.render_to(self.__game.get_screen(), (self.__title_pos_x, self.__title_pos_y), "Don't U",
                                         colors.BLACK)
        self.__font_game_title.render_to(self.__game.get_screen(), (self.__title_pos_x,
                                                                    self.__title_pos_y + self.__new_line_title),
                                         "Panic A**hole", colors.BLACK)
        self.__button_start.draw(events)
        self.__button_controls.draw(events)
        self.__button_exit.draw(events)
