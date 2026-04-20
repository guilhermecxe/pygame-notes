import pygame
from pygame.event import Event

import settings
from scenes.base import Scene
from systems import RenderSystem, InputSystem, MovementSystem
from world import World
from entities import Creature


class GameplayScene(Scene):
    def __init__(self, win):
        self.win = win
        self._done = False
        self.world = World()

        self._setup_world()
        self._setup_systems()

    def _setup_world(self):
        creature_id = self.world.create_entity()
        self.creature = Creature(settings.WIDTH//2, settings.HEIGHT//2, "red")
        self.world.add_component(
            entity_id=creature_id,
            component=self.creature
        )

    def _setup_systems(self):
        self.world.add_system(RenderSystem(self.win, self.creature))
        self.world.add_system(InputSystem())
        self.world.add_system(MovementSystem(self.world, self.creature))

    def update(self, **kwargs):
        self.world.update(**kwargs)

    def is_done(self):
        return self._done