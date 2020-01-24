import socket
import json
import pickle

from threading import Thread
from lib import request_types as request


class Client(Thread):

    def __init__(self, connection, address, requests_dictionary, max_package, server=None):
        Thread.__init__(self)
        self.__connection = connection
        self.__address = address
        self.__requests_dictionary = requests_dictionary
        self.__MAX_PACKAGE = max_package
        self.__server = server
        self.__logged = False
        self.__nick = None
        self.__end = False

    def stop(self):
        self.__end = True

    def login(self, nick):
        self.__logged = True
        self.__nick = nick

    def is_logged(self):
        return self.__logged

    def run(self):
        print(f'open connection {self.__connection}')
        data = True
        while data and not self.__end:
            try:
                self.__connection.settimeout(4)
                data = self.__connection.recv(self.__MAX_PACKAGE)
                if data == b'':
                    break
                deserialized_data = self.__deserialize_object(data)
                request_type = self.__get_request_type(deserialized_data)
                handler = self.__requests_dictionary[request_type]
                respond = handler.handle(deserialized_data, self)
                print('DEBUG', type(respond), ' ', respond)
                self.__connection.sendall(self.__serialize_object(respond))
            except KeyError:
                print('request handler not founded')
                self.__connection.sendall(self.__serialize_object({'respond': 'request cannot be handled}'}))
            except socket.timeout:
                pass
            except Exception as e:
                print(f'Error when handle request {type(e)} {e}')
                break
        print(f'close connection {self.__connection}')
        self.__connection.close()
        self.__server.notify_end_connection(self)

    @staticmethod
    def __get_request_type(data):
        try:
            print(f'Data i Received {data}')
            # mapped_to_json = json.loads(data)
            return data['requestType']
        except KeyError as e:
            print(f'Exception in parsing json file {e}')
            return request.NOT_FOUND

    @staticmethod
    def __serialize_object(sending_object):
        return pickle.dumps(json.dumps(sending_object))

    @staticmethod
    def __deserialize_object(sending_object):
        return json.loads(pickle.loads(sending_object))

