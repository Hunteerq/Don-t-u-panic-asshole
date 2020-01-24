import lib.request_types as request


class Login:

    def __init__(self, auth_key, data):
        self.auth_key = auth_key
        self.type = request.LOGIN
        self.data = data
