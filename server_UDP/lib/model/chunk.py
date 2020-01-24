class Chunk:

    def __init__(self, position):
        self.position = position
        self.object_list = []
        self.characters_list = []

    def add_object(self, obj):
        self.object_list.append(obj)
