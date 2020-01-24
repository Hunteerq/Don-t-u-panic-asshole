import pygame
from lib import colors
import json
import os

game_config = None
file_exists = os.path.isfile("game/config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)
DEFAULT_FONT_STYLE = game_config['monospaced_font'] if game_config is not None else "consolas"
DEFAULT_FONT_SIZE = game_config['interactive_menu_font_size'] if game_config is not None else 20

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 200
DEFAULT_POS_X = 0
DEFAULT_POS_Y = 0
DEFAULT_TEXT_COLOR = colors.BLACK
DEFAULT_MARKED_COLOR = colors.YELLOW
DEFAULT_BACKGROUND_COLOR = colors.GRAY
DEFAULT_CONTENT = ['This is default content. ', 'If you are seeing this, ', 'it means ', 'something went wrong ',
                   'and server list,', "couldn't be downloaded."]


class InteractiveMenu:
    def __init__(self, pos_x=DEFAULT_POS_X, pos_y=DEFAULT_POS_Y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                 content=DEFAULT_CONTENT, text_size=DEFAULT_FONT_SIZE, text_color=DEFAULT_TEXT_COLOR,
                 marked_text_color=DEFAULT_MARKED_COLOR, background_color=DEFAULT_BACKGROUND_COLOR):
        if pos_x < 1:
            suf = pygame.display.get_surface()
            if suf is not None:
                self.__pos_x = pos_x * suf.get_width()
            else:
                self.__pos_x = DEFAULT_POS_X
        else:
            self.__pos_x = pos_x
        if pos_y < 1:
            suf = pygame.display.get_surface()
            if suf is not None:
                self.__pos_y = pos_y * suf.get_height()
            else:
                self.__pos_y = DEFAULT_POS_Y
        else:
            self.__pos_y = pos_y
        if width < 1:
            suf = pygame.display.get_surface()
            if suf is not None:
                self.__width = width * suf.get_width()
            else:
                self.__width = DEFAULT_WIDTH
        else:
            self.__width = width
        if height < 1:
            suf = pygame.display.get_surface()
            if suf is not None:
                self.__height = height * suf.get_height()
            else:
                self.__height = DEFAULT_HEIGHT
        else:
            self.__height = height
        self.__text_size = text_size
        self.__text_color = text_color
        self.__marked_line_color = marked_text_color
        self.__background_color = background_color
        self.__content = content
        self.__text_size = text_size
        self.__marked_line_index = 0
        self.__font_text = pygame.font.SysFont(DEFAULT_FONT_STYLE, self.__text_size)
        self.__top_margin = game_config['interactive_menu_top_margin'] if game_config is not None else 10
        self.__amount_to_print = int((self.__height-self.__top_margin)/self.__text_size)

    def handle_event(self, scroll_surface, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if self.__marked_line_index != 0:
                    self.__marked_line_index = self.__marked_line_index - 1
                    self.fill_surface(scroll_surface)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if self.__marked_line_index != (len(self.__content)-1):
                    self.__marked_line_index = self.__marked_line_index + 1
                    self.fill_surface(scroll_surface)

    def draw(self, events):
        menu_surface = pygame.Surface((self.__width, self.__height))
        menu_surface.fill(self.__background_color)
        menu_rectangle = pygame.Rect(self.__pos_x, self.__pos_y, self.__width, self.__height)
        display_surface = pygame.display.get_surface()
        self.handle_event(menu_surface, events)
        self.fill_surface(menu_surface)
        display_surface.blit(menu_surface, menu_rectangle)

    def fill_surface(self, scroll_surface):
        printed_page = int(self.__marked_line_index/self.__amount_to_print)

        if printed_page*self.__amount_to_print+self.__amount_to_print <= len(self.__content):
            last_to_print = printed_page * self.__amount_to_print + self.__amount_to_print
        else:
            last_to_print = len(self.__content)

        list_to_print = [self.__content[i] for i in range(printed_page*self.__amount_to_print, last_to_print)]
        top_margin = self.__top_margin
        left_margin = game_config['interactive_menu_left_margin'] if game_config is not None else 10
        antialias = True

        for index, server in enumerate(list_to_print, printed_page*self.__amount_to_print):
            if index == self.__marked_line_index:
                scroll_surface.blit(self.__font_text.render(server, antialias, self.__marked_line_color),
                                    (left_margin, top_margin))
            else:
                scroll_surface.blit(self.__font_text.render(server, antialias, self.__text_color),
                                    (left_margin, top_margin))
            top_margin += self.__text_size

    @property
    def get_marked_line_index(self):
        return self.__marked_line_index
