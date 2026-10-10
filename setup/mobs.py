from math import atan2, degrees, hypot
from os import path
from random import randint, uniform, choice
from time import time

import pygame

from setup.bullets import EnemyBullet
from setup.settings import *


class Player:
    def __init__(self, window_size):
        self.window_size = window_size
        self.player_size = player_size

        self.x = self.window_size[0] // 2
        self.y = self.window_size[1] // 2

        self.original_image = pygame.image.load(path.join('assets', 'images', 'player', 'spaceship.png'))
        self.original_image = pygame.transform.scale(self.original_image, self.player_size)
        self.original_image.set_colorkey(white)
        self.original_image = self.original_image.convert_alpha()

        self.image = self.original_image.copy()

        self.mask = pygame.mask.from_surface(self.image)

        self.vel = player_vel

        self.rect = self.image.get_rect()

        self.aiming = False
        self.shooting = False

        self.hp = player_hp

    def bound_to_screen(self):
        if self.x - (self.player_size[0] // 2) <= 0:
            self.x = self.player_size[0] // 2
        if self.x + (self.player_size[0] // 2) >= self.window_size[0]:
            self.x = self.window_size[0] - (self.player_size[0] // 2)
        if self.y - (self.player_size[1] // 2) <= 0:
            self.y = self.player_size[1] // 2
        if self.y + (self.player_size[1] // 2) >= self.window_size[1]:
            self.y = self.window_size[1] - (self.player_size[1] // 2)

    def move(self, dt):
        pos = pygame.mouse.get_pos()

        dx = pos[0] - self.x
        dy = pos[1] - self.y

        angle = degrees(atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)

        self.mask = pygame.mask.from_surface(self.image)

        mouse_presses = pygame.mouse.get_pressed()

        if mouse_presses[2]:
            self.aiming = True
        else:
            self.aiming = False

        if not self.aiming:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.x -= self.vel * dt
            if keys[pygame.K_d]:
                self.x += self.vel * dt
            if keys[pygame.K_w]:
                self.y -= self.vel * dt
            if keys[pygame.K_s]:
                self.y += self.vel * dt

        self.bound_to_screen()

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, window):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        window.blit(self.image, self.rect)

    def update(self, window, dt):
        self.move(dt)
        self.draw(window)


class Enemy:
    def __init__(self, window_size, attack_obj):
        self.window_size = window_size

        self.enemy_size = (randint(50, 100), randint(50, 100))

        side = choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = randint(-self.enemy_size[0] // 2, self.window_size[0] + self.enemy_size[0] // 2)
            self.y = randint(-enemy_spawn_limit + self.enemy_size[1] // 2, -self.enemy_size[1] // 2)
        elif side == 'bottom':
            self.x = randint(-self.enemy_size[0] // 2, self.window_size[0] + self.enemy_size[0] // 2)
            self.y = randint(self.window_size[1] + self.enemy_size[1] // 2,
                             self.window_size[1] + enemy_spawn_limit - self.enemy_size[1] // 2)
        elif side == 'left':
            self.x = randint(-enemy_spawn_limit + self.enemy_size[0] // 2, -self.enemy_size[0] // 2)
            self.y = randint(-self.enemy_size[1] // 2, self.window_size[1] + self.enemy_size[1] // 2)
        elif side == 'right':
            self.x = randint(self.window_size[0] + self.enemy_size[0] // 2,
                             self.window_size[0] + enemy_spawn_limit - self.enemy_size[0] // 2)
            self.y = randint(-self.enemy_size[1] // 2, self.window_size[1] + self.enemy_size[1] // 2)

        self.attack_obj = attack_obj

        self.images = []
        for i in range(20):
            original_image = pygame.image.load(path.join('assets', 'images', 'enemies', f'tiny_ship{i}.png'))
            original_image = pygame.transform.scale(original_image, self.enemy_size)
            original_image.set_colorkey(white)
            original_image = original_image.convert_alpha()
            self.images.append(original_image)

        self.original_image = choice(self.images)
        self.image = self.original_image.copy()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.speed = randint(enemy_low_speed, enemy_top_speed)

        self.last_time_shot = time()
        self.shoot_interval = uniform(0.5, 3.0)
        self.bullets = []

    def draw(self, window):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        window.blit(self.image, self.rect)

    def move(self, dt):
        dx = self.attack_obj.x - self.x
        dy = self.attack_obj.y - self.y

        angle = degrees(atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)

        self.mask = pygame.mask.from_surface(self.image)

        distance = hypot(dx, dy)

        if distance != 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            dir_x = 0
            dir_y = 0

        self.x += dir_x * self.speed * dt
        self.y += dir_y * self.speed * dt

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def shoot(self, window, dt):
        current_time = time()
        if current_time - self.last_time_shot >= self.shoot_interval:
            bullet = EnemyBullet(self.window_size, self.x, self.y, self.attack_obj)
            self.bullets.append(bullet)
            self.last_time_shot = current_time
            self.shoot_interval = uniform(0.5, 3.0)

        for bullet in self.bullets[:]:
            bullet.update(dt)
            bullet.draw(window)
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
            else:
                if bullet.collide():
                    self.attack_obj.hp -= bullet_attack
                    self.bullets.remove(bullet)

    def collide(self):
        offset_x = int(self.rect.left - self.attack_obj.rect.left)
        offset_y = int(self.rect.top - self.attack_obj.rect.top)

        return self.attack_obj.mask.overlap(self.mask, (offset_x, offset_y))

    def update(self, window, dt):
        self.draw(window)
        self.move(dt)
        self.shoot(window, dt)
