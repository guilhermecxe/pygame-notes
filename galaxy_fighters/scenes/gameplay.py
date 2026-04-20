import os

import pygame
from pygame.event import Event

import settings
from components.bullet import Bullet
from components.health import Health
from components.player import Player
from components.sprite import Sprite
from components.transform import Transform
from components.velocity import Velocity
from ecs.world import World
from scenes.base import Scene
from systems.collision import CollisionSystem
from systems.input import InputSystem
from systems.movement import MovementSystem
from systems.render import RenderSystem

_ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


class GameplayScene(Scene):
    def __init__(self, win):
        self.win = win
        self.world = World()
        self._winner_text = ""
        self._done = False

        self._load_assets()
        self._setup_world()
        self._setup_systems()

    def _load_assets(self):
        self.bullet_hit_sound = pygame.mixer.Sound(os.path.join(_ASSETS, "grenade_hit.wav"))
        self.bullet_fire_sound = pygame.mixer.Sound(os.path.join(_ASSETS, "gun_fire.wav"))

        yellow_img = pygame.image.load(os.path.join(_ASSETS, "spaceship_yellow.png"))
        yellow_img = pygame.transform.scale(yellow_img, (settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT))
        self.yellow_img = pygame.transform.rotate(yellow_img, 90)

        red_img = pygame.image.load(os.path.join(_ASSETS, "spaceship_red.png"))
        red_img = pygame.transform.scale(red_img, (settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT))
        self.red_img = pygame.transform.rotate(red_img, -90)

        space_img = pygame.image.load(os.path.join(_ASSETS, "space.png"))
        self.space_img = pygame.transform.scale(space_img, (settings.WIDTH, settings.HEIGHT))

        self.health_font = pygame.font.SysFont("comicsans", 40)
        self.winner_font = pygame.font.SysFont("comicsans", 100)
        self.border = pygame.Rect(
            settings.WIDTH // 2 - settings.BORDER_WIDTH // 2, 0,
            settings.BORDER_WIDTH, settings.HEIGHT,
        )

    def _setup_world(self):
        w = self.world

        yellow = w.create_entity()
        w.add_component(yellow, Transform(
            settings.WIDTH // 4 - settings.SPACESHIP_WIDTH, 300,
            settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT,
        ))
        w.add_component(yellow, Sprite(self.yellow_img))
        w.add_component(yellow, Health(settings.INITIAL_HEALTH))
        w.add_component(yellow, Player(
            tag="yellow",
            move_keys={"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s},
            fire_key=pygame.K_LCTRL,
            fire_direction=1,
        ))

        red = w.create_entity()
        w.add_component(red, Transform(
            settings.WIDTH - settings.WIDTH // 4, 300,
            settings.SPACESHIP_WIDTH, settings.SPACESHIP_HEIGHT,
        ))
        w.add_component(red, Sprite(self.red_img))
        w.add_component(red, Health(settings.INITIAL_HEALTH))
        w.add_component(red, Player(
            tag="red",
            move_keys={"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN},
            fire_key=pygame.K_SPACE,
            fire_direction=-1,
        ))

    def _setup_systems(self):
        self._render = RenderSystem(
            self.win, self.space_img, self.border,
            self.health_font, self.winner_font,
        )
        self.world.add_system(InputSystem(self.bullet_fire_sound))
        self.world.add_system(MovementSystem())
        self.world.add_system(CollisionSystem(self.bullet_hit_sound))
        self.world.add_system(self._render)

    def update(self, events: list[Event]):
        self.world.update(events=events)

        for _, health, player in self.world.query(Health, Player):
            if not health.alive:
                winner = "Red" if player.tag == "yellow" else "Yellow"
                self._winner_text = f"{winner} Wins!"
                self._done = True

    def draw_winner(self):
        self._render.draw_winner(self._winner_text)

    def is_done(self):
        return self._done
