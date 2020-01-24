import pygame
import pygame.freetype
from .colors import *
import json
import os
from lib import gamestates

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

CONTROLS_FONT = game_config['font'] if game_config is not None else "Arial"
CONTROLS_FONT_SIZE = game_config['controls_font_size'] if game_config is not None else 50
CONTROLS_TITLE_SIZE = game_config['controls_title_size'] if game_config is not None else 70


class Controls:

    def __init__(self, game):
        self.__game = game
        self.__size = self.__game.get_screen().get_size()
        self.__menu = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_FONT_SIZE)
        self.__title = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_TITLE_SIZE)
        self.__text = pygame.freetype.SysFont(CONTROLS_FONT, CONTROLS_FONT_SIZE)

        self.equip = pygame.image.load('../game/config/assets/controls/equip.png')
        self.menu = pygame.image.load('../game/config/assets/controls/menu.png')
        self.mouse = pygame.image.load('../game/config/assets/controls/mouse.png')
        self.mouse2 = pygame.image.load('../game/config/assets/controls/mouse2.png')
        self.quick = pygame.image.load('../game/config/assets/controls/quick.png')
        self.use = pygame.image.load('../game/config/assets/controls/use.png')
        self.wasd = pygame.image.load('../game/config/assets/controls/wasd.png')

        self.__title_x = 100
        self.__title_y = self.__size[1] / 8

        self.__first_row_text_y = self.__size[1] / 3 + 160
        self.__first_row_icon_y = self.__size[1] / 3 + 80
        self.__first_row_icon_y2 = self.__size[1] / 3 + 100
        self.__second_row_text_y = self.__size[1] * (3 / 4) + 80

        self.__wsad_length_x = 230
        self.__wsad_length_y = 150
        self.__wsad_icon_x = self.__size[0] / 4 - 45
        self.__wsad_icon_y = self.__size[1] / 3 + 50
        self.__wsad_text_x = self.__size[0] / 4 - 20

        self.__key_length = 70

        self.__equip_icon_x = self.__size[0] / 2 - 40
        self.__equip_text_x = self.__equip_icon_x - 60 - 30

        self.__use_icon_x = self.__size[0] * (3 / 4) - 150
        self.__use_text_x = self.__size[0] * (3 / 4) - 160

        self.__escape_icon_x = self.__size[0] * (3 / 4) + 15
        self.__escape_text_x = self.__escape_icon_x - 30

        self.__access_x_length = 390
        self.__access_y_length = 70
        self.__access_icon_x = self.__size[0] / 4 - 50
        self.__access_icon_y = self.__size[1] * (3 / 4) + 20

        self.__mouse_length = 140
        self.__mouse_icon_y = self.__size[1] * (3 / 4) - 80

        self.__attack_icon_x = self.__size[0] / 2
        self.__attack_text_x = self.__attack_icon_x + 10

        self.__move_icon_x = self.__size[0] * (3 / 4) - 90
        self.__move_text_x = self.__move_icon_x + 45

        self.__exit_x = self.__size[0] * (5 / 6)
        self.__exit_y = self.__size[1] / 8 + 10
        self.__exit_x_length = 100
        self.__exit_y_length = 40
        self.__left_mouse_button = 0
        self.__mouse_x = 0
        self.__mouse_y = 1

    def loop(self):

        self.__game.get_screen().fill(WHITE)

        self.__title.render_to(self.__game.get_screen(), (self.__title_x, self.__title_y), "Controls", BLACK)

        self.__text.render_to(self.__game.get_screen(), (self.__wsad_text_x, self.__first_row_text_y), "Move", BLACK)
        self.__game.get_screen().blit(self.wasd, (self.__wsad_icon_x, self.__wsad_icon_y))

        self.__text.render_to(self.__game.get_screen(), (self.__equip_text_x, self.__first_row_text_y), "Equipment", BLACK)
        self.__game.get_screen().blit(self.equip, (self.__equip_icon_x, self.__first_row_icon_y2))

        self.__text.render_to(self.__game.get_screen(), (self.__use_text_x, self.__first_row_text_y), "Use", BLACK)
        self.__game.get_screen().blit(self.use, (self.__use_icon_x, self.__first_row_icon_y2))

        self.__text.render_to(self.__game.get_screen(), (self.__escape_text_x, self.__first_row_text_y), "Menu", BLACK)
        self.__game.get_screen().blit(self.menu, (self.__escape_icon_x, self.__first_row_icon_y2))

        self.__text.render_to(self.__game.get_screen(), (self.__access_icon_x, self.__second_row_text_y), "Quick access", BLACK)
        self.__game.get_screen().blit(self.quick, (self.__access_icon_x, self.__access_icon_y))

        self.__text.render_to(self.__game.get_screen(), (self.__attack_text_x, self.__second_row_text_y), "Attack", BLACK)
        self.__game.get_screen().blit(self.mouse, (self.__attack_icon_x, self.__mouse_icon_y))

        self.__text.render_to(self.__game.get_screen(), (self.__move_text_x, self.__second_row_text_y), "Aim", BLACK)
        self.__game.get_screen().blit(self.mouse2, (self.__move_icon_x, self.__mouse_icon_y))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.__exit_x + self.__exit_x_length > mouse[self.__mouse_x] > self.__exit_x \
                and self.__exit_y + self.__exit_y_length > mouse[self.__mouse_y] > self.__exit_y:
            self.__menu.render_to(self.__game.get_screen(), (self.__exit_x, self.__exit_y), "Back", GREEN)
            pygame.draw.rect(self.__game.get_screen(), GREEN, (self.__exit_x, self.__exit_y,
                                                               self.__exit_x_length, self.__exit_y_length), 2)
            if click[self.__left_mouse_button]:
                if self.__game.get_last_state() == gamestates.GAME_MENU:
                    self.__game.set_state(gamestates.GAME_MENU)
                else:
                    self.__game.set_state(gamestates.MAIN_MENU)
        else:
            self.__menu.render_to(self.__game.get_screen(), (self.__exit_x, self.__exit_y), "Back", BLACK)
            pygame.draw.rect(self.__game.get_screen(), BLACK, (self.__exit_x, self.__exit_y,
                                                               self.__exit_x_length, self.__exit_y_length), 2)

