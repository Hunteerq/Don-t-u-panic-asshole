from lib.game.items.item import Item
import pygame
import json
import os

item_config = None
file_exists = os.path.isfile("lib/config/items/item_config.json")
if file_exists:
    with open("lib/config/items/item_config.json") as json_file:
        item_config = json.load(json_file)


class Sword(Item):

    def __init__(self):
        self._id = 4
        self._name = 'sword'
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/items/sword.png'),
                                              (item_config['item_sprite_size'], item_config['item_sprite_size']))
        self._action = item_config['melee']
        self._damage = item_config['sword_damage']

