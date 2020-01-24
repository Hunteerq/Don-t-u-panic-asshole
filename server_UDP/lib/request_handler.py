from lib import request_types as request
from lib.model.login import Login
from lib.model.update_position import UpdatePosition
import pickle
import json
import jsonpickle
import time


class RequestHandler:

    def __init__(self, server):
        self.__dictionary = self.__get_dictionary()
        self.__server = server

    def __get_dictionary(self):
        return {
            request.LOGIN: (lambda data, address: self.__handle_login(data, address)),
            request.UPDATE_POSITION: (lambda data, address: self.__handle_position_update(data, address)),
            request.GET_OBJECT: (lambda data, address: self.__handle_get_object(data, address)),
            request.ATTACK: (lambda data, address: self.__handle_attack(data, address))
        }

    def handle_request(self, package):
        data, address = package
        deserialized_data = self.__deserialize_object(data)
        request_type = self.__get_request_type(deserialized_data)
        auth_key = self.__get_key(deserialized_data)
        package_to_send = self.__dictionary[request_type].__call__(deserialized_data, address)
        client = self.__server.get_client_by_key(auth_key)
        if client is not None:
            client.update_last_received_time(time.time())
        return package_to_send

    def __handle_login(self, data, address):
        auth_key = self.__get_key(data)
        data = self.__get_data(data)
        client = self.__server.add_client(data[0], address, auth_key)
        client_character = client.get_client_character()
        all_objects_list = [client_character]
        for obj in self.__server.get_close_objects(client_character):
            all_objects_list.append(obj)
        for character in self.__server.get_close_characters(client_character):
            all_objects_list.append(character)
        data_to_send = self.__serialize_object(Login(auth_key, all_objects_list))
        package_to_send = [(data_to_send, address)]
        return package_to_send

    def __handle_position_update(self, data, address):
        auth_key = self.__get_key(data)
        data = self.__get_data(data)
        if not self.__server.check_user(address, auth_key):
            return None
        client = self.__server.get_client(address, auth_key)
        client_character = client.get_client_character()
        pos_x, pos_y = data
        actual_chunk_index = self.__server.find_chunk_index_by_position(client_character.position)
        next_chunk_index = self.__server.find_chunk_index_by_position((pos_x, pos_y))
        if actual_chunk_index == next_chunk_index:
            client_character.position = (pos_x, pos_y)
        else:
            chunks = self.__server.get_chunks_list()
            chunks[actual_chunk_index].characters_list.remove(client_character)
            client_character.position = (pos_x, pos_y)
            chunks[next_chunk_index].characters_list.append(client_character)
        close_characters = []
        for character in self.__server.get_close_characters(client_character):
            close_characters.append(character)
        package_to_send = []
        for character in close_characters:
            if character != client_character:
                client_to_send = self.__server.find_client_by_character(character)
                data = {
                    "idx": client_character.idx,
                    "position": client_character.position
                }
                data_to_send = self.__serialize_object(UpdatePosition(auth_key, data))
                package_to_send.append((data_to_send, client_to_send.get_address()))
        return package_to_send

    def __handle_get_object(self, data, address):
        auth_key = self.__get_key(data)
        data = self.__get_data(data)
        if not self.__server.check_user(address, auth_key):
            return None
        data_to_send = []
        package_to_send = (data_to_send, address)
        return package_to_send

    def __handle_attack(self, data, address):
        auth_key = self.__get_key(data)
        data = self.__get_data(data)
        if not self.__server.check_user(address, auth_key):
            return None
        data_to_send = []
        package_to_send = (data_to_send, address)
        return package_to_send

    @staticmethod
    def __get_data(data):
        try:
            return data['data']
        except KeyError as e:
            print(f'Exception in parsing json file {e}')
            return None

    @staticmethod
    def __get_key(data):
        try:
            return data['auth_key']
        except KeyError as e:
            print(f'Exception in parsing json file {e}')
            return None

    @staticmethod
    def __get_request_type(data):
        try:
            return data['type']
        except KeyError as e:
            print(f'Exception in parsing json file {e}')
            return None

    @staticmethod
    def __serialize_object(sending_object):
        return pickle.dumps(jsonpickle.encode(sending_object))

    @staticmethod
    def __deserialize_object(sending_object):
        return json.loads(pickle.loads(sending_object))
