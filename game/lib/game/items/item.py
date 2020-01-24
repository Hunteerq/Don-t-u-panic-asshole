class Item:

    _id = None
    _name = None
    _sprite = None
    _action = None
    _damage = None

    def get_name(self):
        return self._name

    def get_sprite(self):
        return self._sprite

    def get_action(self):
        return self._action

    def get_damage(self):
        return self._damage
