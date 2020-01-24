import pygame
import os
import json

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

DEFAULT_WIDTH = 100
DEFAULT_HEIGHT = 50
DEFAULT_POS_X = 0
DEFAULT_POS_Y = 0
DEFAULT_TEXT_SIZE = 34
FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
DEFAULT_BUTTON_BORDER = 0
DEFAULT_BORDER_COLOR = (0, 0, 0)
DEFAULT_HOVER_COLOR = (0, 255, 0, 80)
DEFAULT_NOHOVER_COLOR = (0, 255, 0, 20)
DEFAULT_TEXT_COLOR = (0, 0, 0)


class Button(object):
    def __init__(self, pos_x=DEFAULT_POS_X, pos_y=DEFAULT_POS_Y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, text='',
                 text_size=DEFAULT_TEXT_SIZE, text_color=DEFAULT_TEXT_COLOR,
                 button_border=DEFAULT_BUTTON_BORDER, hover_color=DEFAULT_HOVER_COLOR,
                 nohover_color=DEFAULT_NOHOVER_COLOR, border_color=DEFAULT_BORDER_COLOR, function=None, args=None):
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
        self.__function = function
        self.__text = text
        self.__text_size = text_size
        self.__text_color = text_color
        self.__hover = False
        self.__font_text = pygame.font.SysFont(FONT_STYLE, self.__text_size)
        self.__button_border = button_border
        self.__border_color = border_color
        self.__hover_color = hover_color
        self.__nohover_color = nohover_color
        self.__button_surface = pygame.Surface((self.__width, self.__height))
        self.__button_rect = pygame.Rect(self.__pos_x, self.__pos_y, self.__width, self.__height)
        self.__args = args

    def __check_mouse(self, events):
        for event in events:
            self.__event_handle(event)

    def __event_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.__button_rect.collidepoint(
                pygame.mouse.get_pos()):
            self.__run_function()
        elif self.__button_rect.collidepoint(pygame.mouse.get_pos()):
            self.__hover = True
        else:
            self.__hover = False

    def __run_function(self):
        if self.__function is not None and self.__args is not None:
            self.__function(self.__args)
        elif self.__function is not None and self.__args is None:
            self.__function()

    def set_text(self, text):
        self.__text = text

    def set_hover_color(self, color):
        self.__hover_color = color

    def set_nohover_color(self, color):
        self.__nohover_color = color

    def set_color(self, color):
        self.__hover_color = color
        self.__nohover_color = color

    def __get_text(self):
        button_text = self.__font_text.render(self.__text, True, self.__text_color)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = (self.__pos_x + self.__width / 2, self.__pos_y + self.__height / 2)
        return button_text, button_text_rect

    def draw(self, events):
        self.__check_mouse(events)
        if self.__hover:
            self.__button_surface.fill(self.__hover_color[0:3])
            if len(self.__hover_color) == 4:
                self.__button_surface.set_alpha(self.__hover_color[3])
        else:
            self.__button_surface.fill(self.__nohover_color[0:3])
            if len(self.__nohover_color) == 4:
                self.__button_surface.set_alpha(self.__nohover_color[3])
        if self.__button_border > 0:
            pygame.draw.rect(self.__button_surface, self.__border_color, (0, 0, self.__button_surface.get_width(),
                             self.__button_surface.get_height()), self.__button_border)
        display_surface = pygame.display.get_surface()
        button_text, button_text_rect = self.__get_text()
        display_surface.blit(self.__button_surface,self.__button_rect)
        display_surface.blit(button_text, button_text_rect)
