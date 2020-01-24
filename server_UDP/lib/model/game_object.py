import random


class GameObject(object):
    i = 0

    @staticmethod
    def get_next_id():
        GameObject.i = GameObject.i + 1
        return GameObject.i

    def __init__(self, idx, position, object_type):
        self.idx = idx
        self.position = position
        self.object_type = object_type
        self.sprite = random.randrange(0, 4)

    def get_position(self):
        return self.position
