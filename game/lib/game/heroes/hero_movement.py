CROSS_SPEED = 0.7071
IDLE_SPEED = 0


class HeroMovement:

    @staticmethod
    def movement_right(hero, game):
        hero.set_horizontal_speed(HeroMovement.hero_move_converter(hero, game))
        hero.set_movement_right()

    @staticmethod
    def movement_left(hero, game):
        hero.set_horizontal_speed(-HeroMovement.hero_move_converter(hero, game))
        hero.set_movement_left()

    @staticmethod
    def movement_up(hero, game):
        hero.set_vertical_speed(-HeroMovement.hero_move_converter(hero, game))
        hero.set_movement_up()

    @staticmethod
    def movement_down(hero, game):
        hero.set_vertical_speed(HeroMovement.hero_move_converter(hero, game))
        hero.set_movement_down()

    @staticmethod
    def movement_up_right(hero, game):
        hero.set_movement_right()
        hero.set_movement_up()
        hero.set_vertical_speed(-HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)
        hero.set_horizontal_speed(HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)

    @staticmethod
    def movement_up_left(hero, game):
        hero.set_movement_left()
        hero.set_movement_up()
        hero.set_vertical_speed(-HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)
        hero.set_horizontal_speed(-HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)

    @staticmethod
    def movement_down_right(hero, game):
        hero.set_movement_right()
        hero.set_movement_down()
        hero.set_vertical_speed(HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)
        hero.set_horizontal_speed(HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)

    @staticmethod
    def movement_down_left(hero, game):
        hero.set_movement_left()
        hero.set_movement_down()
        hero.set_vertical_speed(HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)
        hero.set_horizontal_speed(-HeroMovement.hero_move_converter(hero, game) * CROSS_SPEED)

    @staticmethod
    def hero_move_converter(hero, game):
        return hero.get_move_speed() * game.get_delta_time()