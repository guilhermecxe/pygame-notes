from ecs.component import Component


class Sprite(Component):
    def __init__(self, image):
        self.image = image
