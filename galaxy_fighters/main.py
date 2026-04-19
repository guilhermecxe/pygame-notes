import pygame
import os


# Iniciando recursos de som
pygame.mixer.pre_init(
    buffer=256
)

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

pygame.font.init()
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", 'grenade_hit.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("assets", 'gun_fire.wav'))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

SPACESHIP_VEL = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

BULLET_VEL = 7
MAX_BULLETS = 3

# Criando identificadores de eventos personalizados
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("assets", "spaceship_red.png"))
RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(RED_SPACESHIP_IMAGE, -90)

SPACE = pygame.image.load(os.path.join("assets", "space.png"))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        draw_text,
        (WIDTH/2 - draw_text.get_width()//2,
        HEIGHT/2 - draw_text.get_height()//2)
    )
    pygame.display.update()
    pygame.time.delay(5000)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))

    # Borda entre as naves
    pygame.draw.rect(WIN, "black", BORDER)

    # Desenhando a vida das naves
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # As imagens das naves são desenhadas sempre onde estão os retângulos red e yellow
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and (yellow.x - SPACESHIP_VEL) > 0: # left
        yellow.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_d] and (yellow.x + yellow.width + SPACESHIP_VEL) < BORDER.x: # right
        yellow.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_w] and (yellow.y - SPACESHIP_VEL) > 0: # up
        yellow.y -= SPACESHIP_VEL
    if keys_pressed[pygame.K_s] and (yellow.y + SPACESHIP_VEL + yellow.height) < HEIGHT: # down
        yellow.y += SPACESHIP_VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and (red.x - SPACESHIP_VEL) > BORDER.x + BORDER.width: # left
        red.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + red.width + SPACESHIP_VEL) < WIDTH: # right
        red.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_UP] and (red.y - SPACESHIP_VEL) > 0: # up
        red.y -= SPACESHIP_VEL
    if keys_pressed[pygame.K_DOWN] and (red.y + SPACESHIP_VEL + red.height) < HEIGHT: # down
        red.y += SPACESHIP_VEL

def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(WIDTH - WIDTH / 4, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WIDTH / 4 - YELLOW_SPACESHIP_IMAGE.get_width(), 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                # Criando os torpedos (bullets)
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height//2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height//2,
                        10,
                        5,
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        
        draw_window(
            red, yellow, red_bullets, yellow_bullets,
            red_health, yellow_health
        )

    # Reiniciando o jogo se ele parar com break
    main()


if __name__ == "__main__":
    main()