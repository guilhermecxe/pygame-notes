from components.bullet import Bullet
from components.health import Health
from components.player import Player
from components.transform import Transform
import settings


class CollisionSystem:
    def __init__(self, bullet_hit_sound):
        self.bullet_hit_sound = bullet_hit_sound

    def update(self, world, events=None):
        players = {
            player.tag: (transform, health)
            for _, player, transform, health in world.query(Player, Transform, Health)
        }

        to_remove = []
        for eid, bullet, transform in world.query(Bullet, Transform):
            rect = transform.rect

            if rect.x > settings.WIDTH or rect.x + rect.width < 0:
                to_remove.append(eid)
                continue

            target_tag = "red" if bullet.owner == "yellow" else "yellow"
            if target_tag not in players:
                continue

            target_transform, target_health = players[target_tag]
            if target_transform.rect.colliderect(rect):
                target_health.hp -= 1
                self.bullet_hit_sound.play()
                to_remove.append(eid)

        for eid in to_remove:
            world.remove_entity(eid)
