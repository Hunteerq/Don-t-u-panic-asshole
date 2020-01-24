import random

from lib.model.game_object import GameObject

X_INDEX = 0
Y_INDEX = 1


class Villain(GameObject):

    def __init__(self, idx, position, object_type, drop_items, health_points, attack, move_speed):
        super(Villain, self).__init__(idx, position, object_type)
        self.__next_position = position
        self.__drop_items = drop_items
        self.__health_points = health_points
        self.__attack = attack
        self.__move_speed = move_speed

    def set_new_position(self, new_x, new_y):
        self.__next_position = [new_x, new_y]

    def random_move(self):
        if self.position == self.__next_position:
            self.__get_new_position()

    def __get_new_position(self):
        new_x, new_y = random.randint(-100, 100), random.randint(-100, 100)
        current_position = self.position
        if current_position[X_INDEX] + new_x > 50000 or current_position[X_INDEX] + new_x < 0:
            new_x = 0
        if current_position[Y_INDEX] + new_y > 50000 or current_position[Y_INDEX] + new_y < 0:
            new_y = 0
        self.set_new_position(current_position[X_INDEX] + new_x, current_position[Y_INDEX] + new_y)

    def move_object(self):
        self.__handle_cords(X_INDEX)
        self.__handle_cords(Y_INDEX)

    def __handle_cords(self, index):
        if self.__next_position[index] > self.position[index]:
            self.position[index] += self.__move_speed
            if self.position[index] > self.__next_position[index]:
                self.position[index] = self.__next_position[index]
        else:
            self.position[index] -= self.__move_speed
            if self.position[index] < self.__next_position[index]:
                self.position[index] = self.__next_position[index]



