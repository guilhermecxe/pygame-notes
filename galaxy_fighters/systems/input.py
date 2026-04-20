import pygame
from components.bullet import Bullet
from components.player import Player
from components.transform import Transform
from components.velocity import Velocity
import settings


class InputSystem:
    def __init__(self, bullet_fire_sound):
        self.bullet_fire_sound = bullet_fire_sound

    def update(self, world, events=None):
        if not events:
            return

        bullet_counts = {"yellow": 0, "red": 0}
        for _, bullet in world.query(Bullet):
            bullet_counts[bullet.owner] += 1

        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            for _, player, transform in world.query(Player, Transform):
                if event.key != player.fire_key:
                    continue
                if bullet_counts[player.tag] >= settings.MAX_BULLETS:
                    continue

                rect = transform.rect
                bx = rect.x + rect.width if player.fire_direction > 0 else rect.x
                by = rect.y + rect.height // 2

                bullet_eid = world.create_entity()
                world.add_component(bullet_eid, Transform(bx, by, 10, 5))
                world.add_component(bullet_eid, Velocity(dx=settings.BULLET_VEL * player.fire_direction))
                world.add_component(bullet_eid, Bullet(player.tag, player.fire_direction))
                self.bullet_fire_sound.play()
                bullet_counts[player.tag] += 1
