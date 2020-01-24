import json
import os
from math import floor

import pygame
import pygame.freetype

from lib import colors
from lib import gamestates

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

FONT_SIZE = game_config['creators_font_size'] if game_config is not None else 20
PADDING = game_config['creators_padding'] if game_config is not None else 10
FONT_STYLE = game_config['creators_font_style'] if game_config is not None else "freesansbold.ttf"
LEFT_PADDING = 6
VELOCITY = 100


class CreatorsMenu:

    def __init__(self, game):
        self.__game = game
        self.__game.get_screen().fill(colors.BLACK)
        self.__screen_size = self.__game.get_screen().get_size()
        self.__buffer = []
        self.__read_text()
        self.__text = []
        self.__start_y = self.__screen_size[1]
        self.__start_x = floor(self.__screen_size[0] / LEFT_PADDING)
        self.__font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.__end_loop_condition = 0
        self.__prepare_text()
        self.__position = 0

    def loop(self):
        events = self.__game.get_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__reset_state()
                self.__game.set_state(gamestates.MAIN_MENU)
                return

        delta_time = self.__game.get_delta_time()
        if self.__position < self.__end_loop_condition:
            self.__position += (delta_time * VELOCITY)
            self.__game.get_screen().fill(colors.BLACK)
            self.__write_text(self.__start_y - self.__position)
        else:
            self.__reset_state()
            self.__game.set_state(gamestates.MAIN_MENU)
            return

    def __read_text(self):
        with open(r"lib/resources/final_credits.txt", encoding="utf8") as file:
            for line in file:
                self.__buffer.append(line.strip())
        file.close()

    def __write_text(self, y):
        for element in self.__text:
            self.__game.get_screen().blit(element, (self.__start_x, y))
            y += FONT_SIZE + PADDING

    def __prepare_text(self):
        line_count = 0
        for element in self.__buffer:
            line_count += 1
            if element != '':
                if element[0] == '-':
                    self.__text.append(self.__font.render(element, True, colors.GREEN, colors.BLACK))
                else:
                    self.__text.append(self.__font.render(element, True, colors.WHITE, colors.BLACK))
            else:
                self.__text.append(self.__font.render(element, True, colors.GREEN, colors.BLACK))

        self.__end_loop_condition = self.__screen_size[1] + line_count * (FONT_SIZE + PADDING)

    def __reset_state(self):
        self.__position = 0
