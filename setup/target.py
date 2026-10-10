from os import path

import pygame

from setup.settings import *


class Target:
    def __init__(self, control):
        self.control = control
        self.target_size = target_size

        self.mouse_pos = pygame.mouse.get_pos()

        self.yellow_image = pygame.image.load(path.join('assets', 'images', 'targets', 'yellow_target.png'))
        self.yellow_image = pygame.transform.scale(self.yellow_image, self.target_size)
        self.yellow_image = self.yellow_image.convert_alpha()

        self.red_image = pygame.image.load(path.join('assets', 'images', 'targets', 'red_target.png'))
        self.red_image = pygame.transform.scale(self.red_image, self.target_size)
        self.red_image = self.red_image.convert_alpha()

        self.x = self.mouse_pos[0]
        self.y = self.mouse_pos[1]

        self.rect = self.yellow_image.get_rect(center=(self.x, self.y))

    def draw(self, window):
        if self.control.aiming:
            window.blit(self.red_image, self.rect)
        else:
            window.blit(self.yellow_image, self.rect)

    def move(self):
        self.mouse_pos = pygame.mouse.get_pos()

        self.x = self.mouse_pos[0]
        self.y = self.mouse_pos[1]

        self.rect = self.yellow_image.get_rect(center=(self.x, self.y))

    def update(self, window):
        self.draw(window)
        self.move()
