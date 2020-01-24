from lib.connections.request import request_types


class Login:

    def __init__(self, username, password):
        self.requestType = request_types.LOGIN
        self.username = username
        self.password = password
