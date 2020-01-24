import pygame
import json
import os

from lib import gamestates
from lib import interactive_menu
from lib import colors

game_config = None
file_exists = os.path.isfile("game/config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)
FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
FONT_SIZE = game_config['intro_font_size'] if game_config is not None else 50


class ServerList:
    def __init__(self, game):
        self.__menu_title = "Servers"
        self.__game = game
        self.__tcp_connector = self.__game.get_tcp_connector()
        self.__active_server = 0
        self.__title = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        self.__server_list = None
        self.__server_strings = None
        self.__interactive_menu = None
        self.__try_again = False

    def loop(self):
        if self.__server_list is None or self.__try_again is True:
            self.__server_list = self.__tcp_connector.get_servers(1)
            self.__server_strings = self.__refacotr_strings(self.__server_list)
            if not self.__server_list:
                self.__interactive_menu = interactive_menu.InteractiveMenu(0.25, 0.2, 0.5, 0.6)
                self.__try_again = True
            else:
                self.__interactive_menu = interactive_menu.InteractiveMenu(0.25, 0.2, 0.5, 0.6, self.__server_strings)
                self.__try_again = False

        events = self.__game.get_events()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__game.set_state(gamestates.MAIN_MENU)
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.__server_list:
                    self.__active_server = self.__interactive_menu.get_marked_line_index
                    self.__game.set_state(gamestates.GAME)

        self.__generate_view(events)

    def __generate_view(self, events):
        display_surface = pygame.display.get_surface()
        title = self.__title.render("Select game server", True, colors.BLACK)
        title_rect = title.get_rect()
        title_rect.center = (display_surface.get_width() / 2, display_surface.get_height() * 0.1)
        display_surface.blit(title, title_rect)
        self.__interactive_menu.draw(events)

    def __refacotr_strings(self, server_list):
        servers_strings = []
        first_row_length = 20
        second_row_length = 34
        for server in server_list:
            server_info = ''
            i = 0
            for server_parameter in server:
                string_to_add = str(server_parameter)
                if i == 0:
                    while len(string_to_add) < first_row_length:
                        string_to_add += ' '
                elif i == 1:
                    while len(string_to_add) < second_row_length:
                        string_to_add += ' '
                server_info += string_to_add
                i += 1

            servers_strings.append(server_info)
        return servers_strings
