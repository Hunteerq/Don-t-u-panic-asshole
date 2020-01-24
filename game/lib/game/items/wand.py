from lib.game.items.item import Item
import pygame
import json
import os

item_config = None
file_exists = os.path.isfile("lib/config/items/item_config.json")
if file_exists:
    with open("lib/config/items/item_config.json") as json_file:
        item_config = json.load(json_file)


class Wand(Item):

    def __init__(self):
        self._id = 5
        self._name = 'wand'
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/items/wand.png'),
                                              (item_config['item_sprite_size'], item_config['item_sprite_size']))
        self._action = item_config['distance']
        self._damage = item_config['wand_damage']

