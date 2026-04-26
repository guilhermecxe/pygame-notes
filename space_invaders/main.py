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

# Player ships
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
PLAYER_VEL = 5

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.image.load(os.path.join("assets", "background-black.png"))
BG = pygame.transform.scale(BG, (settings.WIDTH, settings.HEIGHT))

main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 60)

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
        window.blit(self.ship_img, (self.x, self.y))
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50), 0)

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.max_health = health
 
        # Criando uma superfície de colisão equivalente com os pixels da imagem
        self.mask = pygame.mask.from_surface(self. ship_img)

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.max_health = health

        # Criando uma superfície de colisão equivalente com os pixels da imagem
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def update(lives, level, players, enemies: list[Enemy], lost: bool):
    WIN.blit(BG, (0, 0))

    lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (settings.WIDTH - level_label.get_width() - 10, 10))

    for enemy in enemies:
        enemy.draw(WIN)

    players.draw(WIN)

    if lost:
        lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
        WIN.blit(lost_label, (settings.WIDTH/2 - lost_label.get_width()/2, 350))

    pygame.display.update()

def run():
    clock = pygame.time.Clock()
    level = 0
    lives = 5

    enemies: list[Enemy] = []
    wave_length = 5
    enemy_vel = 1

    player = Player(300, 650)

    run = True
    lost = False
    while run:
        clock.tick(settings.FPS)

        if lives <= 0 or player.health == 0:
            lost = True

        # Se não houverem mais inimigos, aumentamos o nível e criamos novos
        if not enemies:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    x=random.randrange(100, settings.WIDTH-100),
                    y=random.randrange(-1500, -100),
                    color=random.choice(["red", "blue", "green"]) 
                )
                enemies.append(enemy)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL > 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.get_width() + PLAYER_VEL < settings.WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL > 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.get_height() < settings.HEIGHT:
            player.y += PLAYER_VEL

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > settings.HEIGHT:
                # Um inimigo passou -> menos uma vida
                lives -= 1
                enemies.remove(enemy)

        update(lives, level, player, enemies, lost)

    pygame.quit()

if __name__ == "__main__":
    run()