import pygame
from ecs.component import Component


class Transform(Component):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
