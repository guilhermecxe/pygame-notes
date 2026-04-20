import pygame
from components.bullet import Bullet
from components.health import Health
from components.player import Player
from components.sprite import Sprite
from components.transform import Transform
import settings


class RenderSystem:
    def __init__(self, win, space_img, border, health_font, winner_font):
        self.win = win
        self.space_img = space_img
        self.border = border
        self.health_font = health_font
        self.winner_font = winner_font

    def update(self, world, events=None):
        self.win.blit(self.space_img, (0, 0))
        pygame.draw.rect(self.win, settings.BLACK, self.border)

        for _, player, health in world.query(Player, Health):
            text = self.health_font.render(f"Health: {health.hp}", 1, settings.WHITE)
            if player.tag == "yellow":
                self.win.blit(text, (10, 10))
            else:
                self.win.blit(text, (settings.WIDTH - text.get_width() - 10, 10))

        for _, sprite, transform in world.query(Sprite, Transform):
            self.win.blit(sprite.image, transform.rect.topleft)

        for _, bullet, transform in world.query(Bullet, Transform):
            color = settings.YELLOW if bullet.owner == "yellow" else settings.RED
            pygame.draw.rect(self.win, color, transform.rect)

        pygame.display.update()

    def draw_winner(self, text):
        surface = self.winner_font.render(text, 1, settings.WHITE)
        x = settings.WIDTH // 2 - surface.get_width() // 2
        y = settings.HEIGHT // 2 - surface.get_height() // 2
        self.win.blit(surface, (x, y))
        pygame.display.update()
        pygame.time.delay(5000)
