import time
import random

ACTIVE_TIME_IN_SECONDS = 10
MIN_NEXT_SEND_DELAY = 2000
MAX_NEXT_SEND_DELAY = 2500
MILLISECONDS_IN_SECOND = 1000


class Client:

    def __init__(self, nick, address, auth_key, client_character):
        self.__nick = nick
        self.__address = address
        self.__auth_key = auth_key
        self.__last_received_time = time.time()
        self.__client_character = client_character
        self.__next_update_time = None
        self.generate_next_update_time()

    def get_client_character(self):
        return self.__client_character

    def get_address(self):
        return self.__address

    def generate_next_update_time(self):
        self.__next_update_time = time.time() + \
                                  (random.randrange(MIN_NEXT_SEND_DELAY, MAX_NEXT_SEND_DELAY) /
                                   MILLISECONDS_IN_SECOND)

    def need_update(self):
        current_time = time.time()
        if current_time > self.__next_update_time:
            return True
        else:
            return False

    def get_auth_key(self):
        return self.__auth_key

    def update_last_received_time(self, received_time):
        self.__last_received_time = received_time

    def is_user_active(self):
        current_time = time.time()
        if current_time - self.__last_received_time > ACTIVE_TIME_IN_SECONDS:
            return False
        else:
            return True
