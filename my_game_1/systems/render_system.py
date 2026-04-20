import pygame
from pygame.surface import Surface

from entities import Creature

class RenderSystem:
    def __init__(self, win: Surface, creature: Creature):
        self.win = win
        self.creature = creature

    def update(self, **kwargs):
        self.win.fill("white")

        self.creature.draw(self.win)
        
        pygame.display.update()
