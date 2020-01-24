from threading import Thread
import socket

RECEIVE_TIMEOUT = 10


class ReceivePackagesThread(Thread):
    
    def __init__(self, sock, q, max_package):
        Thread.__init__(self)
        self.__socket = sock
        self.__queue = q
        self.__max_package = max_package
        self.__running = True

    def stop(self):
        self.__running = False

    def run(self):
        self.__socket.settimeout(RECEIVE_TIMEOUT)
        while self.__running:
            self.__get_package()

    def __get_package(self):
        try:
            package = self.__socket.recvfrom(self.__max_package)
            if package:
                self.__put_message(package)
        except socket.timeout:
            pass
        except Exception as e:
            print(f'Error receiving data from clients {e}')

    def __put_message(self, package):
        self.__queue.put(package)


class SendPackagesThread(Thread):
    
    def __init__(self, sock, q):
        Thread.__init__(self)
        self.__socket = sock
        self.__queue = q
        self.__running = True

    def stop(self):
        self.__running = False

    def run(self):
        while self.__running:
            self.__send_package()

    def __send_package(self):
        while not self.__queue.empty():
            data, address = self.__queue.get()
            self.__socket.sendto(data, address)
