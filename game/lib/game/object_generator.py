from lib.game.world_objects.rock import Rock
from lib.game.world_objects.tree import Tree
from random import randint

# this class exists purely for testing purpose, objects will be generated based on database records in future
coordinate_x = [10, 0, -30, 200, -90, 320, 410, 118, -175, -281, 600, -800, 90, 19, 28]
coordinate_y = [-400, 300, 200, -200, 450, 352, 503, 244, 175, 344, 900, 800, -300, 600, -690]


class ObjectGenerator:

    @staticmethod
    def generate_objects():
        object_list = []
        for i in range(15):
            type = randint(0, 1) 
            if type == 0:
                object_list.append(Rock(0, coordinate_x[i], coordinate_y[i]))
            elif type == 1:
                object_list.append(Tree(0, coordinate_x[i], coordinate_y[i]))
        return object_list
