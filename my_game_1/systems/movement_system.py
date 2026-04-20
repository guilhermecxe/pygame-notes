from entities import Creature

import pygame


class MovementSystem:
    def __init__(self, world, creature: Creature):
        self.world = world
        self.creature = creature

    def update(self, **kwargs):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.creature.x -= 5
        if keys[pygame.K_RIGHT]:
            self.creature.x += 5
        if keys[pygame.K_UP]:
            self.creature.y -= 5
        if keys[pygame.K_DOWN]:
            self.creature.y += 5
