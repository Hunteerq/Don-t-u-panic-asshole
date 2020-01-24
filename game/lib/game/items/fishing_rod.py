from lib.game.items.item import Item
import pygame
import os
import json

item_config = None
file_exists = os.path.isfile("lib/config/items/item_config.json")
if file_exists:
    with open("lib/config/items/item_config.json") as json_file:
        item_config = json.load(json_file)


class FishingRod(Item):

    def __init__(self):
        self._id = 3
        self._name = 'fishing_rod'
        self._sprite = pygame.transform.scale(pygame.image.load('config/assets/items/fishing_rod.png'),
                                              (item_config['item_sprite_size'], item_config['item_sprite_size']))


