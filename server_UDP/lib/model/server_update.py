import lib.request_types as request


class ServerUpdate:

    def __init__(self, auth_key, data):
        self.auth_key = auth_key
        self.type = request.SERVER_UPDATE
        self.data = data
