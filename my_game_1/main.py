import pygame

import settings
from scenes.gameplay import GameplayScene

pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("My Game 1")


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
            
        scene.update(events=events)
            
if __name__ == "__main__":
    run()