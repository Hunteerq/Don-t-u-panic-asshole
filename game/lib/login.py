import pygame
import os
import json
from lib import gamestates
from lib import input
from lib import button
from lib import colors
from lib.connections.request import request_types

game_config = None
file_exists = os.path.isfile("config/game_config.json")
if file_exists:
    with open("config/game_config.json") as json_file:
        game_config = json.load(json_file)

FONT_STYLE = game_config['font'] if game_config is not None else "Segoe UI"
FONT_SIZE = game_config['login_font_size'] if game_config is not None else 50


class Login(object):
    def __init__(self, game):
        self.__game = game
        self.__title = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        self.__input_login = input.Input(0.25, 0.3, 0.5, 0.1, 'Username')
        self.__input_password = input.Input(0.25, 0.5, 0.5, 0.1, 'Password', is_password=True)
        self.__login_button = button.Button(0.25, 0.65, 0.5, 0.1, text='LOGIN', function=self.__send_login_request)
        self.__info = button.Button(0.1, 0.85, 0.8, 0.1, text='Enter your username and password',
                                    function=self.__hide_info, hover_color=colors.GREEN, nohover_color=colors.GREEN,
                                    button_border=1)
        self.__show_info = True
        self.__waiting_for_server_response = False
        print("Login initialized")

    def __hide_info(self):
        self.__show_info = False
        self.__info.set_text('')

    def __validate_input(self, login, password):
        if login == '' and password == '':
            self.__info.set_text('You need to type something')
            self.__info.set_color(colors.YELLOW)
            self.__show_info = True
            return False
        elif login == '':
            self.__info.set_text('Enter username')
            self.__info.set_color(colors.YELLOW)
            self.__show_info = True
            return False
        elif password == '':
            self.__info.set_text('Enter password')
            self.__info.set_color(colors.YELLOW)
            self.__show_info = True
            return False
        return True

    def __send_login_request(self):
        login = self.__input_login.get_value()
        password = self.__input_password.get_value()
        if not self.__validate_input(login, password):
            return
        conn = self.__game.get_tcp_connector()
        if not conn.is_connected():
            self.__info.set_text('No server connection. Try again later.')
            self.__info.set_color(colors.RED)
            self.__show_info = True
            return
        if conn.login_authorize(login, password):
            print("Send login request")
            self.__waiting_for_server_response = True

    def __check_server_response(self):
        server_responses = self.__game.get_tcp_server_responses()
        for response in server_responses:
            if response['request_type'] != request_types.LOGIN_RESULT:
                continue
            if response['response'] == 'True':
                print("Login success")
                self.__game.set_logged_user(self.__input_login.get_value())
                self.__game.set_state(gamestates.MAIN_MENU)
                self.__waiting_for_server_response = False
            else:
                print("Login failure")
                self.__info.set_text('Wrong username or password')
                self.__info.set_color(colors.RED)
                self.__show_info = True
                self.__waiting_for_server_response = False

    def loop(self):
        if self.__waiting_for_server_response:
            self.__check_server_response()
        events = self.__game.get_events()
        display_surface = pygame.display.get_surface()
        title = self.__title.render("Don\'t u panic a**hole", True, colors.BLACK)
        title_rect = title.get_rect()
        title_rect.center = (display_surface.get_width() / 2, display_surface.get_height() * 0.1)
        display_surface.blit(title, title_rect)
        if self.__show_info:
            self.__info.draw(events)
        self.__input_login.draw(events)
        self.__input_password.draw(events)
        self.__login_button.draw(events)
