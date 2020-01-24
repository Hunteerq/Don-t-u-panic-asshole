import pygame
import json
import os
import threading
import queue
import time

from lib import gamestates
from lib import intro
from lib import login
from lib import colors
from lib.game.game_runner import GameRunner
from lib.music import MenuMusic
from lib import main_menu
from lib import server_list
from lib import creators_menu
from lib import controls
from lib.connections import connector
from lib.connections import udp_connector
from lib.connections.request import request_types
from lib.game_menu import GameMenu
import random

QUEUE_SIZE = 20
RECONNECT_TRY_DELAY = 10
GET_RESPONSE_TIMEOUT = 2
GET_UDP_RESPONSE_TIMEOUT = 0.1
SECOND_IN_MILLISECONDS = 1000.0


class TcpConnectionThread(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.__game = game
        self.__last_reconnect_try = time.process_time()

    def run(self):
        conn = self.__game.get_tcp_connector()
        while not self.__game.tcp_thread_status():
            if not self.__check_server_connection(conn):
                continue
            response = conn.get_response(timeout=GET_RESPONSE_TIMEOUT)
            if response is not False:
                self.__game.tcp_queue_put(response)
        print('tcp thread terminated')

    def __check_server_connection(self, conn):
        if not conn.is_connected():
            if time.process_time() - self.__last_reconnect_try > RECONNECT_TRY_DELAY:
                conn.try_reconnect()
            return False
        else:
            return True


class UdpConnectionThread(threading.Thread):

    def __init__(self, game):
        threading.Thread.__init__(self)
        self.__game = game

    def run(self):
        print('udp started')
        last_received = time.time()
        udp_conn = self.__game.get_udp_connector()
        key = random.randint(0, 100)
        self.__game.set_key(key)
        udp_conn.send_packet(request_types.UDP_LOGIN, [self.__game.get_logged_user()], key)
        while not self.__game.udp_thread_status():
            response = udp_conn.get_response(timeout=GET_UDP_RESPONSE_TIMEOUT)
            if response is not False:
                self.__game.udp_queue_put(response)
                last_received = time.time()
            if time.time() - last_received > 10:
                self.__game.set_state(gamestates.MAIN_MENU)
                self.__game.stop_udp()
        print('udp thread terminated')
        self.__game.remove_udp_thread()


class UdpSenderThread(threading.Thread):
    def __init__(self, game, main_hero):
        threading.Thread.__init__(self)
        self.__game = game
        self.__hero = main_hero

    def run(self):
        conn = self.__game.get_udp_connector()
        last_send = time.time()
        key = self.__game.get_key()
        while not self.__game.udp_thread_status():
            if time.time() - last_send > 0.1:
                x = self.__hero.get_x()
                y = self.__hero.get_y()
                data = [x, y]
                conn.send_packet(request_types.UDP_UPDATE_POSITION, data, key)

                last_send = time.time()
        print('sender thread terminated')


class Game:
    def __init__(self):
        self.__game_title = 'Dont\'t u panic asshole'
        self.__settings = None
        self.__settings_file = "./settings.json"
        self.__state = None
        self.__clock = None
        self.__screen = None
        self.__events = None
        self.__tcp_connector = connector.Connector()
        self.__udp_connector = udp_connector.UdpConnector()
        self.__tcp_queue = queue.Queue(QUEUE_SIZE)
        self.__udp_queue = queue.Queue(QUEUE_SIZE)
        self.__tcp_server_responses = []
        self.__udp_server_responses = []
        self.__tcp_thread = TcpConnectionThread(self)
        self.__udp_thread = None
        self.__udp_send_thread = None
        self.__tcp_thread_stop = False
        self.__udp_thread_stop = False
        self.__logged_user = None
        self.__tcp_thread.start()
        self.__key = None
        self.__last_state = None

    def set_key(self, key):
        self.__key = key

    def get_key(self):
        return self.__key

    def get_last_state(self):
        return self.__last_state

    def set_last_state(self, state):
        self.__last_state = state

    def pass_hero(self, hero):
        self.__udp_send_thread = UdpSenderThread(self, hero)
        self.__udp_send_thread.start()

    def remove_udp_thread(self):
        self.__udp_thread = None
        self.__udp_thread_stop = False

    def tcp_thread_status(self):
        return self.__tcp_thread_stop

    def udp_thread_status(self):
        return self.__udp_thread_stop

    def stop_udp(self):
        self.__udp_thread_stop = True

    def get_tcp_connector(self):
        return self.__tcp_connector

    def set_logged_user(self, user):
        self.__logged_user = user

    def get_logged_user(self):
        return self.__logged_user

    def get_udp_connector(self):
        return self.__udp_connector

    def tcp_queue_put(self, data):
        self.__tcp_queue.put(data)

    def udp_queue_put(self, data):
        self.__udp_queue.put(data)

    def get_tcp_server_responses(self):
        return self.__tcp_server_responses

    def __get_data_from_tcp_queue(self):
        self.__tcp_server_responses.clear()
        while not self.__tcp_queue.empty():
            self.__tcp_server_responses.append(self.__tcp_queue.get())

    def get_udp_server_responses(self):
        return self.__udp_server_responses

    def __get_data_from_udp_queue(self):
        self.__udp_server_responses.clear()
        while not self.__udp_queue.empty():
            self.__udp_server_responses.append(self.__udp_queue.get())

    def get_screen(self):
        return self.__screen

    def get_events(self):
        return self.__events

    def update_events(self):
        self.__events = pygame.event.get()

    def get_settings(self):
        file_exists = os.path.isfile(self.__settings_file)
        if not file_exists:
            self.crash("Settings file does not exists")
        with open(self.__settings_file) as json_file:
            data = json.load(json_file)
        self.__settings = data
        return data

    def init(self):
        if self.__settings is None:
            self.get_settings()
        width = self.__settings['width']
        height = self.__settings['height']
        if self.__settings['fullscreen']:
            display_mode = pygame.FULLSCREEN
        else:
            display_mode = 0
        self.__clock = pygame.time.Clock()
        pygame.init()
        self.__screen = pygame.display.set_mode((width, height), display_mode)
        pygame.display.set_caption(self.__game_title)
        if self.__settings['intro_enable']:
            self.__state = gamestates.INTRO
        else:
            self.__state = gamestates.LOGIN
        print("Game initialized")

    def get_state(self):
        return self.__state

    def handle_quit_event(self):
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.set_state(gamestates.QUIT)

    def set_state(self, state):
        self.__state = state

    def tick(self):
        pygame.display.flip()
        self.__clock.tick_busy_loop(self.__settings['fps_max'])
        self.__get_data_from_tcp_queue()
        self.__get_data_from_udp_queue()
        self.__screen.fill(colors.WHITE)

    def get_delta_time(self):
        return self.__clock.get_time() / SECOND_IN_MILLISECONDS

    def quit(self):
        self.__tcp_thread_stop = True
        self.__udp_thread_stop = True
        print("Bye bye :(")
        pygame.quit()
        exit(0)

    def crash(self, msg):
        self.__tcp_thread_stop = True
        self.__udp_thread_stop = True
        print(msg)
        pygame.quit()
        exit(-1)

    def create_udp_connection_thread(self):
        if self.__udp_thread is None:
            self.__udp_thread = UdpConnectionThread(self)
            self.__udp_thread.start()


if __name__ == "__main__":
    main = Game()
    main.init()
    music_obj = MenuMusic()
    intro_obj = intro.Intro(main)
    login_obj = login.Login(main)
    main_menu_obj = main_menu.MainMenu(main)
    creators_menu_obj = creators_menu.CreatorsMenu(main)
    server_list_obj = server_list.ServerList(main)
    game_menu_obj = GameMenu(main)
    settings_obj = None
    settings_controls_obj = controls.Controls(main)
    settings_video_obj = None
    settings_audio_obj = None
    creators_obj = None
    game_obj = GameRunner(main)
    music_obj.start_music()
    while True:
        main.update_events()
        main.handle_quit_event()
        if main.get_state() == gamestates.QUIT:
            main.quit()
        elif main.get_state() == gamestates.INTRO:
            intro_obj.loop()
        elif main.get_state() == gamestates.LOGIN:
            login_obj.loop()
        elif main.get_state() == gamestates.MAIN_MENU:
            main_menu_obj.loop()
        elif main.get_state() == gamestates.SERVER_LIST:
            server_list_obj.loop()
        elif main.get_state() == gamestates.SETTINGS:
            pass
        elif main.get_state() == gamestates.SETTINGS_VIDEO:
            pass
        elif main.get_state() == gamestates.CONTROLS:
            settings_controls_obj.loop()
        elif main.get_state() == gamestates.SETTINGS_AUDIO:
            pass
        elif main.get_state() == gamestates.CREATORS:
            creators_menu_obj.loop()
        elif main.get_state() == gamestates.GAME:
            music_obj.stop_music()
            game_obj.loop()
        elif main.get_state() == gamestates.GAME_MENU:
            game_menu_obj.loop()
        else:
            main.crash("Unknown game state")
        main.tick()
