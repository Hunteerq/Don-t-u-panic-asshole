import pygame


class MenuMusic:

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('config/music/main_menu_music.mp3')  #Sample song

    # noinspection PyMethodMayBeStatic
    def start_music(self):
        pygame.mixer.music.play()

    # noinspection PyMethodMayBeStatic
    def stop_music(self):
        pygame.mixer.music.stop()
