import pygame

from setup.settings import *


class HealthBar:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, window, hp):
        pygame.draw.rect(window, red, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(window, green, (self.x, self.y, hp, self.h))
        pygame.draw.rect(window, blue, (self.x, self.y, self.w, self.h), 5)

    def update(self, window, hp):
        self.draw(window, hp)
