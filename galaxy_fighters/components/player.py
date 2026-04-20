from ecs.component import Component


class Player(Component):
    def __init__(self, tag, move_keys, fire_key, fire_direction):
        self.tag = tag                  # "yellow" or "red"
        self.move_keys = move_keys      # dict with keys: left, right, up, down
        self.fire_key = fire_key
        self.fire_direction = fire_direction  # +1 or -1
