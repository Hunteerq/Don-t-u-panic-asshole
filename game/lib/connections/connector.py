import socket
import pickle
import json
from lib import errors_provider
from lib.connections.request.login_data import Login
from lib.connections.request.server_list import ServerList
from lib.connections.request import request_types


class Connector:

    def __init__(self):
        self.__SERVER_IP_ADDRESS = None
        self.__SERVER_PORT = None
        self.__MAX_PACKAGE = None
        self.__socket = None
        self.__is_connected = False
        self.__server_config_file_dir = "config/server_config.json"
        self.__read_config()
        self.__bind_socket()

    def try_reconnect(self):
        self.__bind_socket()
        return self.__is_connected

    def is_connected(self):
        return self.__is_connected

    def __read_config(self):
        try:
            with open(self.__server_config_file_dir) as json_file:
                config_file = json.load(json_file)
                self.__SERVER_IP_ADDRESS = config_file['ipAddress']
                self.__SERVER_PORT = config_file['portNumber']
                self.__MAX_PACKAGE = config_file['maxPackage']
        except Exception as e:
            print(f'Error reading config file {e}')
            exit(errors_provider.CONFIG_ERROR)

    def __bind_socket(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__SERVER_IP_ADDRESS, self.__SERVER_PORT))
            self.__is_connected = True
        except socket.error as exc:
            self.__is_connected = False
            print(f'Exception while connecting to server {exc}')

    def login_authorize(self, username, password):
        authorized_user = Login(username, password)
        try:
            self.__socket.sendall(self.__serialize_object(authorized_user))
        except Exception as e:
            self.__is_connected = False
            print(f'Error sending data from server (Login) {e}')
            return False
        return True

    def get_servers(self, timeout=None):
        servers_list = ServerList()
        try:
            self.__socket.sendall(self.__serialize_object(servers_list))
            if timeout is not None:
                self.__socket.settimeout(timeout)
            server_response = self.__socket.recv(self.__MAX_PACKAGE)
            if server_response == '':
                return []
            else:
                server_response = self.__deserialize_object(server_response)
            print(f'Server responded with {server_response}')
            if server_response['request_type'] == request_types.SERVER_LISTS:
                return server_response['response']
        except socket.timeout:
            self.__socket.settimeout(None)
        except Exception as e:
            print(f'Error sending and receiving data from server (Server list) {e}')
        return []
        pass

    def get_response(self, timeout=None):
        try:
            if timeout is not None:
                self.__socket.settimeout(timeout)
            server_response = self.__socket.recv(self.__MAX_PACKAGE)
            self.__socket.settimeout(None)
            if server_response == '':
                self.__is_connected = False
                return False
            else:
                server_response = self.__deserialize_object(server_response)
            print(f'Server responded with {server_response}')
            return server_response
        except socket.timeout:
            self.__socket.settimeout(None)
        except Exception as e:
            self.__is_connected = False
            print(f'Error receiving data from server (Login) {e}')
        return False

    @staticmethod
    def __serialize_object(sending_object):
        return pickle.dumps(json.dumps(vars(sending_object)))

    @staticmethod
    def __deserialize_object(sending_object):
        return json.loads(pickle.loads(sending_object))

