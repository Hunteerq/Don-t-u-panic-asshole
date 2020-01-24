from lib.model.game_object import GameObject


class Water(GameObject):

    def __init__(self, idx, position, object_type):
        super(Water, self).__init__(idx, position, object_type)
