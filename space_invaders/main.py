import pygame
import random
import time
import os

import settings

pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
PLAYER_VEL = 5

# Lasers
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, (settings.WIDTH, settings.HEIGHT))

main_font = pygame.font.SysFont("comicsans", 50)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)


def update(lives, level, ship):
    WIN.blit(BG, (0, 0))

    lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (settings.WIDTH - level_label.get_width() - 10, 10))

    ship.draw(WIN)

    pygame.display.update()

def run():
    clock = pygame.time.Clock()
    level = 1
    lives = 5

    ship = Ship(300, 650)

    run = True
    while run:
        clock.tick(settings.FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            ship.x += PLAYER_VEL
        if keys[pygame.K_UP]:
            ship.y -= PLAYER_VEL
        if keys[pygame.K_DOWN]:
            ship.y += PLAYER_VEL

        update(lives, level, ship)

    pygame.quit()

if __name__ == "__main__":
    run()