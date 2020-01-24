import pygame
import json
import os
from lib import gamestates
from lib import colors

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
FONT_SIZE = game_config['intro_font_size'] if game_config is not None else 50
INTRO_DURATION = game_config['intro_duration'] if game_config is not None else 6000
TEXT_TO_SHOW = ["Grupa 32", "Presents", "Don\'t u panic a**hole"]


class Intro(object):
    def __init__(self, game):
        self.__game = game
        self.__time_start = pygame.time.get_ticks()
        self.__intro_duration = INTRO_DURATION
        self.__texts = TEXT_TO_SHOW
        self.__font = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        print("Intro initialized")

    def loop(self):
        events = self.__game.get_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__game.set_state(gamestates.LOGIN)
                return
        time_from_start = pygame.time.get_ticks() - self.__time_start
        if time_from_start >= self.__intro_duration:
            self.__game.set_state(gamestates.LOGIN)
            return
        label = self.__font.render(self.__texts[time_from_start // (self.__intro_duration // len(self.__texts))], 1, colors.BLACK)
        label_rect = label.get_rect(center=(self.__game.get_screen().get_width() / 2, self.__game.get_screen().get_height() / 2))
        self.__game.get_screen().blit(label, label_rect)
