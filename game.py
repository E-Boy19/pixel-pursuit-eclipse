import sys
from os import path

import pygame

from setup.bullets import Bullet
from setup.explosion import Explosion
from setup.file_edit import create_dir, load_high_score, save_high_score
from setup.health import HealthBar
from setup.mobs import Player, Enemy
from setup.settings import *
from setup.target import Target

pygame.init()
pygame.display.init()
pygame.font.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_size = self.screen.get_size()
        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]

        pygame.display.set_caption('Pixel Pursuit : Eclipse')

        pygame.mouse.set_visible(False)

        create_dir()

        self.clock = pygame.time.Clock()

        self.l_font = pygame.font.Font(path.join('assets', 'fonts', 'font.ttf'), l_font)
        self.m_font = pygame.font.Font(path.join('assets', 'fonts', 'font.ttf'), m_font)
        self.s_font = pygame.font.Font(path.join('assets', 'fonts', 'font.ttf'), s_font)

        self.paused = False

        self.bg_image = pygame.image.load(path.join('assets', 'images', 'background', 'bg.jpg'))
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen_size)
        self.bg_image = self.bg_image.convert_alpha()

        self.bg_start_image = pygame.image.load(path.join('assets', 'images', 'background', 'bg_start.jpg'))
        self.bg_start_image = pygame.transform.scale(self.bg_start_image, self.screen_size)
        self.bg_start_image = self.bg_start_image.convert_alpha()

        self.start_image = pygame.image.load(path.join('assets', 'images', 'background', 'start.png'))
        self.start_image = pygame.transform.scale(self.start_image, (750, 750))
        self.start_image.set_colorkey(black)
        self.start_image = self.start_image.convert_alpha()
        self.start_image_rect = self.start_image.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2))

        self.player = Player(self.screen_size)
        self.target = Target(self.player)

        self.enemies = []
        for i in range(enemy_count):
            enemy = Enemy(self.screen_size, self.player)
            self.enemies.append(enemy)

        self.player_bullets = []

        self.player_health = HealthBar(10, 10, player_hp, 50)

        self.score = 0
        self.highscore = load_high_score()

        self.explosions = []

        self.bullet_sound = pygame.mixer.Sound(path.join('assets', 'sounds', 'laser.mp3'))
        self.enemy_unalive_sound = pygame.mixer.Sound(path.join('assets', 'sounds', 'enemy_blast.mp3'))
        self.player_unalive_sound = pygame.mixer.Sound(path.join('assets', 'sounds', 'player_blast.mp3'))

        self.player_explosion = None
        self.player_unalive = False

        self.playing = True

        self.start = False
        self.died = False

    def draw_center_text(self, font, text, text_color, center_pos):
        text = font.render(text, True, text_color)
        text_rect = text.get_rect(center=center_pos)
        self.screen.blit(text, text_rect)

    def draw_right_text(self, font, text, text_color, pos):
        text = font.render(text, True, text_color)
        text_size = text.get_size()
        self.screen.blit(text, (pos[0] - text_size[0], pos[1]))

    def draw_bg(self):
        self.screen.blit(self.bg_image, (0, 0))

    def draw(self, dt):
        self.draw_bg()

        for enemy in self.enemies[:]:
            enemy.update(self.screen, dt)
            if enemy.collide():
                self.player.hp -= enemy_attack
                self.enemies.remove(enemy)
                self.enemies.append(Enemy(self.screen_size, self.player))
                exp = Explosion(enemy.x, enemy.y, 'e')
                self.explosions.append(exp)
                self.enemy_unalive_sound.play()
            for bullet in self.player_bullets[:]:
                if bullet.collide(enemy):
                    self.score += 1
                    if not bullet.aiming_when_fired:
                        self.player_bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.enemies.append(Enemy(self.screen_size, self.player))
                    exp = Explosion(enemy.x, enemy.y, 'e')
                    self.explosions.append(exp)
                    self.enemy_unalive_sound.play()

        for bullet in self.player_bullets[:]:
            bullet.update(dt)
            bullet.draw(self.screen)

        for explosion in self.explosions[:]:
            explosion.update(dt)
            explosion.draw(self.screen)
            if explosion.finished:
                self.explosions.remove(explosion)

        self.player.update(self.screen, dt)
        self.target.update(self.screen)

        self.draw_right_text(self.s_font, f'SCORE:{self.score}', white, (self.screen_size[0], 10))
        self.draw_right_text(self.s_font, f'HIGHSCORE:{self.highscore}', white, (self.screen_size[0], 60))

        self.player_health.update(self.screen, self.player.hp)

    def show_paused_screen(self):
        self.draw_center_text(self.l_font, 'PAUSED', blue, (self.screen_width // 2, self.screen_height // 3))
        self.draw_center_text(self.s_font, 'CLICK ANYWHERE TO UNPAUSE', white,
                              (self.screen_width // 2, (self.screen_height // 3) + 100))

        pygame.display.update()

    def update(self, dt):
        self.draw(dt)

        pygame.display.update()

    def reset(self):
        self.player = Player(self.screen_size)
        self.target = Target(self.player)

        self.enemies = []
        for i in range(enemy_count):
            enemy = Enemy(self.screen_size, self.player)
            self.enemies.append(enemy)

        self.player_bullets = []

        self.player_health = HealthBar(10, 10, player_hp, 50)

        self.score = 0

        self.paused = False
        self.died = False
        self.start = False
        self.player_unalive = False
        self.player_explosion = None

    def show_death_screen(self):
        self.draw_right_text(self.s_font, f'SCORE:{self.score}', white, (self.screen_size[0], 10))
        self.draw_right_text(self.s_font, f'HIGHSCORE:{self.highscore}', white, (self.screen_size[0], 60))

        self.draw_center_text(self.l_font, 'GAME OVER', white, (self.screen_size[0] // 2, self.screen_size[1] // 3))

        self.draw_center_text(self.s_font, 'PRESS SPACE TO PLAY AGAIN', white,
                              (self.screen_size[0] // 2, (self.screen_size[1] // 3) + 100))
        self.draw_center_text(self.s_font, 'PRESS ESCAPE TO QUIT', white,
                              (self.screen_size[0] // 2, (self.screen_size[1] // 3) + 150))

        pygame.display.update()

    def show_start_screen(self):
        self.screen.fill(black)

        self.screen.blit(self.bg_start_image, (0, 0))

        self.screen.blit(self.start_image, self.start_image_rect)

        self.draw_center_text(self.s_font, 'PRESS SPACE TO PLAY', white,
                              (self.screen_size[0] // 2, self.screen_size[1] - 50))

        pygame.display.update()

    def show_start_menu(self):
        running = True
        while running:
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.playing = False
                    if event.key == pygame.K_SPACE:
                        self.start = True
                        running = False

            self.show_start_screen()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.paused:
                        running = False
                        self.playing = False
                    if event.key == pygame.K_ESCAPE and not self.paused:
                        self.paused = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0] and len(self.player_bullets) < max_bullets:
                        bullet = Bullet(self.screen_size, self.player, self.target, self.player_bullets)
                        self.player_bullets.append(bullet)
                        self.bullet_sound.play()
                    if mouse_presses[0] and self.paused:
                        self.paused = False

            if self.highscore <= self.score:
                self.highscore = self.score
                save_high_score(self.highscore)

            if self.player.hp <= 0 and not self.player_unalive:
                self.player_unalive_sound.play()
                self.player_explosion = Explosion(self.player.x, self.player.y, 'p')
                self.player_unalive = True

            if self.player_unalive:
                if self.player_explosion:
                    self.player_explosion.update(dt)
                    self.draw_bg()
                    for explosion in self.explosions[:]:
                        explosion.update(dt)
                        explosion.draw(self.screen)
                        if explosion.finished:
                            self.explosions.remove(explosion)
                    self.player_explosion.draw(self.screen)
                    pygame.display.update()
                    if self.player_explosion.finished:
                        running = False
                        self.died = True
                continue

            if self.paused:
                self.show_paused_screen()
                continue

            self.update(dt)

    def show_end_menu(self):
        running = True
        while running:
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.playing = False
                    if event.key == pygame.K_SPACE:
                        self.start = True
                        self.died = False
                        running = False

            self.show_death_screen()

    def start_game(self):
        while self.playing:
            self.show_start_menu()
            if self.start:
                self.run()
            if self.died:
                self.show_end_menu()
                self.reset()


if __name__ == '__main__':
    game = Game()

    game.start_game()

    pygame.quit()
    sys.exit()
