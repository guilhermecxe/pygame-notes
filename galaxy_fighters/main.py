import pygame

import settings
from scenes.gameplay import GameplayScene

pygame.mixer.pre_init(buffer=256)
pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Galaxy Fighters")


def run():
    clock = pygame.time.Clock()
    scene = GameplayScene(WIN)

    while True:
        clock.tick(settings.FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        scene.update(events)

        if scene.is_done():
            scene.draw_winner()

            # Criando nova cena de gameplay para iniciar o jogo novamente
            scene = GameplayScene(WIN)


if __name__ == "__main__":
    run()
