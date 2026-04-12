import pygame
import time
import random

pygame.font.init() # Necessário para utilizar fontes

WIDTH, HEIGHT = 1000, 800 # tamanho da janela em pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # cria a janela do jogo
pygame.display.set_caption("Space Dodge") # título da janela

image = pygame.image.load("space_dodge/background.png")
BG = pygame.transform.scale(image, (WIDTH, HEIGHT)) # escala a imagem para o tamanho especificado com distorção

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player: pygame.Rect, elapsed_time: float, stars: list[pygame.Rect]):
    WIN.blit(BG, (0, 0)) # posiciona a imagem no local especificado

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update() # atualiza a tela para exibir a alteração

def main():
    run = True

    player = pygame.Rect(
        200, # left, 200 pixels à direita do ponto 0
        HEIGHT - PLAYER_HEIGHT, # top, encostado na parte inferior
        PLAYER_WIDTH, # width
        PLAYER_HEIGHT # height
    )

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000 # a cada quantos ms uma estrela será adicionada
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        # clock.tick regula a quantidade de frames por segundo independente da máquina
        # clock.tick também retorna a quantidade de milissegundos desde o último tick
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT) # -STAR_HEIGHT faz começar fora da tela
                stars.append(star)

            # Diminuimos star_add_increment por 50 a cada geração de estrelas
            # até que o valor chegue a 200. Isso faz com que o intervalo de geração de estrelas
            # aconteça cada vez mais rápido
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # As posições .x e .y de um objeto apontam para o canto superior esquerdo
        # dele. Então, por exemplo, player.x + player.width aponta para a extrema direita dele
         
        # Capturando teclas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.width + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL

        # Movendo as estrelas
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT: # se saiu da tela
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): # se atingiu o player
                stars.remove(star)
                hit = True
                break # player atingido, não tem mais ponto em continuar processando as estrelas

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            # Posicionando o texto no centro
            WIN.blit(
                lost_text,
                (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)
            )
            pygame.display.update()
            pygame.time.delay(4000) # Pausa em milissegundos
            break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()
