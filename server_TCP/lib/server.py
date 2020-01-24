import socket
import os
import sys
import json

from threading import Thread, Lock

from lib.request_entities import request_factory as request_factory
from lib import errors_provider as error

from lib.db.db_connection import DataBase
from lib.client import Client


class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__IP_ADDRESS = None
        self.__PORT_NUMBER = None
        self.__MAX_HOSTS = None
        self.__MAX_PACKAGE = None
        self.__socket = None
        self.__login_request_handler = None
        self.__server_list_request_handler = None
        self.__connected_clients = []
        self.__config_file = 'config/server_config.json'
        self.__read_config()
        self.__db = DataBase()
        self.__requests_dictionary = request_factory.get_request_dictionary(self.__db)
        self.__bind_socket()
        self.__stopped = False
        self.__stop_signal_lock = Lock()
        self.__client_list_lock = Lock()

    def stop(self):
        self.__stop_signal_lock.acquire()
        self.__stopped = True
        self.__stop_signal_lock.release()

    def run(self):
        self.__listen_for_connections()

    def __check_stop(self):
        self.__stop_signal_lock.acquire()
        result = self.__stopped
        self.__stop_signal_lock.release()
        return result

    def __read_config(self):
        if os.path.isfile(self.__config_file):
            with open(self.__config_file) as json_file:
                config_file = json.load(json_file)
                self.__IP_ADDRESS = config_file['ipAddress']
                self.__PORT_NUMBER = config_file['portNumber']
                self.__MAX_HOSTS = config_file['maxHosts']
                self.__MAX_PACKAGE = config_file['maxPackage']
        else:
            self.__handle_config_from_console()

    def __handle_config_from_console(self):
        print('There is no config file for server! Pass me interface, port number and max hosts')
        self.__IP_ADDRESS = input('Enter host IP x.x.x.x: ')
        self.__PORT_NUMBER = int(input('Enter port number: '))
        self.__MAX_HOSTS = int(input('Enter max hosts to connect with: '))

    def __bind_socket(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.bind((self.__IP_ADDRESS, self.__PORT_NUMBER))
        except socket.error as msg:
            print(f'Failed binding specified interface {self.__IP_ADDRESS} and port {self.__PORT_NUMBER} error {msg}')
            sys.exit(error.WRONG_SOCKET)

    def __close_server(self):
        self.__client_list_lock.acquire()
        for client in self.__connected_clients:
            client.stop()
        client_copy = self.__connected_clients.copy()
        self.__client_list_lock.release()

        print("DEBUG waiting for close connections by clients")
        for client in client_copy:
            client.join(timeout=8)

        self.__client_list_lock.acquire()
        client_count = len(self.__connected_clients)
        self.__client_list_lock.release()

        if client_count == 0:
            print("DEBUG all clients successful end connection")
        else:
            print("DEBUG: " + str(client_count) + " clients cannot be closed normal")
        self.__db.close_connection()
        print("DEBUG end server thread")

    def __listen_for_connections(self):
        self.__socket.listen(self.__MAX_HOSTS)
        print('Server initialized')
        while not self.__check_stop():
            try:
                self.__socket.settimeout(1)
                connection, address = self.__socket.accept()
                client = Client(connection, address, self.__requests_dictionary, self.__MAX_PACKAGE, self)
                client.start()
                self.__connected_clients.append(client)
            except socket.timeout:
                pass
            except Exception as e:
                print("unexpected error server will be stopped" + str(e))
                self.__stopped = True
        self.__close_server()

    def notify_end_connection(self, client):
        self.__client_list_lock.acquire()
        self.__connected_clients.remove(client)
        self.__client_list_lock.release()
