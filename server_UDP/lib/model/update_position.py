import lib.request_types as request


class UpdatePosition:

    def __init__(self, auth_key, data):
        self.auth_key = auth_key
        self.type = request.UPDATE_POSITION
        self.data = data
