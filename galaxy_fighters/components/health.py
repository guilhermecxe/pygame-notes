from ecs.component import Component


class Health(Component):
    def __init__(self, hp):
        self.hp = hp

    @property
    def alive(self):
        return self.hp > 0
