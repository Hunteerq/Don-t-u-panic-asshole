

class Packet:

    data = []

    def __init__(self, request_type, data: [], key):
        self.type = str(request_type)
        self.data = data
        self.auth_key = str(key)

