from lib.game.items.item import Item
import pygame
import json
import os

item_config = None
file_exists = os.path.isfile("lib/config/items/item_config.json")
if file_exists:
    with open("lib/config/items/item_config.json") as json_file:
        item_config = json.load(json_file)


class Equipment:

    __item_list = [None, None, None, None, None]
    __background = pygame.transform.scale(pygame.image.load('config/assets/item_background.png'),
                                          (item_config['item_sprite_size'], item_config['item_sprite_size']))
    __marked_background = pygame.transform.scale(pygame.image.load('config/assets/marked_item_background.png'),
                                                 (item_config['item_sprite_size'], item_config['item_sprite_size']))
    __marked_index = 0

    def pick_up_item(self, new_item: Item):
        index = self.__item_list.index(None) if None in self.__item_list else None
        if index is not None:
            self.__item_list.insert(index, new_item)
            print("Item placed in eq on slot number:" + str(index))
        else:
            print("Inventory is full")
            
    def get_background(self):
        return self.__background

    def get_marked_background(self):
        return self.__marked_background

    def get_item_by_index(self, index):
        return self.__item_list[index]

    def drop_item(self, index):
        self.__item_list.insert(index, None)

    def get_items(self):
        return self.__item_list

    def mark_item(self, index):
        self.__marked_index = index

    def get_marked_index(self):
        return self.__marked_index

