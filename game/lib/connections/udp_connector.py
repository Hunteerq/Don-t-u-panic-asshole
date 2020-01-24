import socket
import pickle
import json
import random
from lib import errors_provider
from lib.connections.request.packet import Packet


class UdpConnector:
    def __init__(self):
        self.__SERVER_IP_ADDRESS = None
        self.__SERVER_PORT = None
        self.__MAX_PACKAGE = None
        self.__socket = None
        self.__server_config_file_dir = "config/server_config.json"
        self.__read_config()
        self.__bind_socket()

    def __read_config(self):
        try:
            with open(self.__server_config_file_dir) as json_file:
                config_file = json.load(json_file)
                self.__SERVER_IP_ADDRESS = config_file['ipAddress']
                self.__SERVER_PORT = config_file['udpPortNumber']
                self.__MAX_PACKAGE = config_file['maxPackage']
        except Exception as e:
            print(f'Error reading config file {e}')
            exit(errors_provider.CONFIG_ERROR)

    def __bind_socket(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def get_response(self, timeout=None):
        if self.__socket is None:
            print('elo')
        try:
            if timeout is not None:
                self.__socket.settimeout(timeout)
            server_response, _ = self.__socket.recvfrom(self.__MAX_PACKAGE)
            self.__socket.settimeout(None)
            if server_response == '':
                return False
            else:
                server_response = self.__deserialize_object(server_response)
                print(f'Server responded with {server_response}')
            return server_response
        except socket.timeout:
            self.__socket.settimeout(None)
            return False
        except Exception as e:
            print(f'Error receiving data from server {e}')
        return False

    def send_packet(self, request_type, data: [], auth_key):
        packet = Packet(request_type, data, auth_key)
        try:
            self.__socket.sendto(self.__serialize_object(packet), (self.__SERVER_IP_ADDRESS, self.__SERVER_PORT))
        except Exception as e:
            print(f'Error sending data to server (Packet with objects id) {e}')
            return False
        return True

    @staticmethod
    def __serialize_object(sending_object):
        return pickle.dumps(json.dumps(vars(sending_object)))

    @staticmethod
    def __deserialize_object(sending_object):
        return json.loads(pickle.loads(sending_object))
