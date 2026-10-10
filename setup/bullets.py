from math import atan2, degrees, hypot
from os import path
from random import uniform, choice

import pygame

from setup.settings import *


class EnemyBullet:
    def __init__(self, window_size, x, y, target):
        self.window_size = window_size
        self.x = x
        self.y = y
        self.target = target

        self.bullet_size = bullet_size

        self.original_image = pygame.image.load(path.join('assets', 'images', 'bullets', 'enemy_bullet.png'))
        self.original_image = pygame.transform.scale(self.original_image, self.bullet_size)
        self.original_image.set_colorkey(white)
        self.original_image = self.original_image.convert_alpha()

        self.image = self.original_image.copy()

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        angle = degrees(atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.radius = enemy_bullet_radius
        self.speed = enemy_bullet_speed

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        distance = hypot(dx, dy)

        if distance == 0:
            distance = 1

        self.dir_x = dx / distance
        self.dir_y = dy / distance

        self.inaccuracy_x = choice([uniform(-0.15, -0.05), uniform(0.05, 0.15)])
        self.inaccuracy_y = choice([uniform(-0.15, -0.05), uniform(0.05, 0.15)])

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, dt):
        self.x += (self.dir_x + self.inaccuracy_x) * self.speed * dt
        self.y += (self.dir_y + self.inaccuracy_y) * self.speed * dt

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def is_off_screen(self):
        return (
                self.x + self.radius < 0 or self.x - self.radius > self.window_size[0] or
                self.y + self.radius < 0 or self.y - self.radius > self.window_size[1]
        )

    def collide(self):
        if self.rect.colliderect(self.target):
            offset_x = int(self.rect.left - self.target.rect.left)
            offset_y = int(self.rect.top - self.target.rect.top)

            return self.target.mask.overlap(self.mask, (offset_x, offset_y))

        return False

    def update(self, dt):
        self.move(dt)


class Bullet:
    def __init__(self, window_size, control, target, bullets_list):
        self.window_size = window_size

        self.control = control
        self.target = target

        self.bullets = bullets_list

        self.x = self.control.x
        self.y = self.control.y

        self.bullet_size = bullet_size

        self.original_yellow_image = pygame.image.load(path.join('assets', 'images', 'bullets', 'yellow_bullet.png'))
        self.original_yellow_image = pygame.transform.scale(self.original_yellow_image, self.bullet_size)
        self.original_yellow_image.set_colorkey(white)
        self.original_yellow_image = self.original_yellow_image.convert_alpha()

        self.yellow_image = self.original_yellow_image.copy()

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        angle = degrees(atan2(-dy, dx))
        self.yellow_image = pygame.transform.rotate(self.original_yellow_image, angle - 90)

        self.original_red_image = pygame.image.load(path.join('assets', 'images', 'bullets', 'red_bullet.png'))
        self.original_red_image = pygame.transform.scale(self.original_red_image, self.bullet_size)
        self.original_red_image.set_colorkey(white)
        self.original_red_image = self.original_red_image.convert_alpha()

        self.red_image = self.original_red_image.copy()

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        angle = degrees(atan2(-dy, dx))
        self.red_image = pygame.transform.rotate(self.original_red_image, angle - 90)

        self.mask = pygame.mask.from_surface(self.yellow_image)

        self.rect = self.yellow_image.get_rect(center=(self.x, self.y))

        self.yellow_radius = yellow_bullet_radius
        self.red_radius = red_bullet_radius

        self.speed = yellow_bullet_speed

        dx = self.target.x - self.x
        dy = self.target.y - self.y

        distance = hypot(dx, dy)
        if distance == 0:
            distance = 1

        self.dir_x = dx / distance
        self.dir_y = dy / distance

        self.aiming_when_fired = self.control.aiming

        if not self.aiming_when_fired:
            self.inaccuracy_x = choice([uniform(-0.15, -0.05), uniform(0.05, 0.15)])
            self.inaccuracy_y = choice([uniform(-0.15, -0.05), uniform(0.05, 0.15)])
        else:
            self.inaccuracy_x = 0
            self.inaccuracy_y = 0

        if self.aiming_when_fired:
            self.speed = red_bullet_speed
        else:
            self.speed = yellow_bullet_speed

    def draw(self, window):
        if not self.aiming_when_fired:
            window.blit(self.yellow_image, (self.x, self.y))
        else:
            window.blit(self.red_image, (self.x, self.y))

        self.control.shooting = True

    def move(self, dt):
        if self.control.shooting:
            self.x += (self.dir_x + self.inaccuracy_x) * self.speed * dt
            self.y += (self.dir_y + self.inaccuracy_y) * self.speed * dt

        if not self.aiming_when_fired:
            self.rect = self.yellow_image.get_rect(center=(self.x, self.y))
            self.mask = pygame.mask.from_surface(self.yellow_image)
        else:
            self.rect = self.red_image.get_rect(center=(self.x, self.y))
            self.mask = pygame.mask.from_surface(self.red_image)

    def is_off_screen(self):
        if not self.aiming_when_fired:
            return ((self.x + self.yellow_radius <= 0) or (self.x - self.yellow_radius >= self.window_size[0]) or
                    (self.y + self.yellow_radius <= 0) or (self.y - self.yellow_radius >= self.window_size[1]))
        else:
            return ((self.x + self.red_radius <= 0) or (self.x - self.red_radius >= self.window_size[0]) or
                    (self.y + self.red_radius <= 0) or (self.y - self.red_radius >= self.window_size[1]))

    def collide(self, enemy):
        if self.rect.colliderect(enemy.rect):
            offset_x = int(self.rect.left - enemy.rect.left)
            offset_y = int(self.rect.top - enemy.rect.top)

            return enemy.mask.overlap(self.mask, (offset_x, offset_y))

        return False

    def unalive(self):
        self.bullets.remove(self)

    def update(self, dt):
        if self.is_off_screen():
            self.unalive()
            return
        self.move(dt)
