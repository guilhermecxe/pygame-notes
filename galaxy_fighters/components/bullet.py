from ecs.component import Component


class Bullet(Component):
    def __init__(self, owner, direction):
        self.owner = owner      # "yellow" or "red"
        self.direction = direction  # +1 moves right, -1 moves left
