import pygame
from components.player import Player
from components.transform import Transform
from components.velocity import Velocity
import settings

_BORDER_X = settings.WIDTH // 2 - settings.BORDER_WIDTH // 2


class MovementSystem:
    def update(self, world, events=None):
        for _, vel, transform in world.query(Velocity, Transform):
            transform.rect.x += vel.dx
            transform.rect.y += vel.dy

        keys = pygame.key.get_pressed()
        for _, player, transform in world.query(Player, Transform):
            rect = transform.rect
            km = player.move_keys
            v = settings.SPACESHIP_VEL

            if player.tag == "yellow":
                x_min, x_max = 0, _BORDER_X
            else:
                x_min, x_max = _BORDER_X + settings.BORDER_WIDTH, settings.WIDTH

            if keys[km["left"]] and rect.x - v >= x_min:
                rect.x -= v
            if keys[km["right"]] and rect.x + rect.width + v <= x_max:
                rect.x += v
            if keys[km["up"]] and rect.y - v >= 0:
                rect.y -= v
            if keys[km["down"]] and rect.y + rect.height + v <= settings.HEIGHT:
                rect.y += v
