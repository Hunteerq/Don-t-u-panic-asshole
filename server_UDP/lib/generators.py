import random
from lib.object_types import ObjectTypes
from lib.model.game_object import GameObject

MIN_WATER_PLACE_COUNT = 5
MAX_WATER_PLACE_COUNT = 100

MIN_ITEMS_COUNT = 1000
MAX_ITEMS_COUNT = 1100

MAP_HEIGHT = 50000
MAP_WIDTH = 50000


class MapGenerator(object):
    @staticmethod
    def generate_objects_list():
        list = []
        object_types_count = ObjectTypes.OBJECT_TYPES_COUNT.value
        print(object_types_count)
        for i in range(random.randrange(MIN_ITEMS_COUNT, MAX_ITEMS_COUNT)):
            list.append(GameObject(GameObject.get_next_id(),
                                   (random.randrange(0, MAP_HEIGHT), random.randrange(0, MAP_WIDTH)),
                                   random.randrange(2, object_types_count)))

        return list
