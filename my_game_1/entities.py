import pygame


_next_id = 0
def new_entity():
    global _next_id
    _next_id += 1
    return _next_id


class Creature:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 10, 10))
