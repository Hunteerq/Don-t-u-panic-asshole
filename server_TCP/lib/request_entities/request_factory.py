from abc import ABC, abstractmethod

from lib import request_types


def get_request_dictionary(db):
    return {
        request_types.LOGIN: LoginRequestHandler(db),
        request_types.GET_SERVERS: ServerList(db),
    }


class RequestHandler(ABC):

    def __init__(self, db):
        self._DB = db

    @abstractmethod
    def handle(self, data, client):
        pass


class LoginRequestHandler(RequestHandler):

    def handle(self, data, client):
        user = data['username']
        password = data['password']
        (result,) = \
            self._DB.make_query(f"SELECT count(*) FROM player where password = '{password}' and nick='{user}'")[0]
        if result == 1:
            print('user ' + user + '  log in')
            client.login(user)
            return {"request_type": request_types.LOGIN_RESULT, "response": 'True'}
        elif result == 0:
            print('user ' + user + '  fail log in')
            return {"request_type": request_types.LOGIN_RESULT, "response": 'False'}
        else:
            raise ImportError('data base return inconsistency result')


class ServerList(RequestHandler):

    def handle(self, data, client):
        if client.is_logged():
            server_list = self._DB.make_query(f"SELECT name, server_ip, player_count FROM server")
            return {"request_type": request_types.SERVER_LISTS, "response": server_list}
        else:
            raise IllegalAccessException


class IllegalAccessException(Exception):
    pass
