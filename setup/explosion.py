from os import path

from setup.settings import *
from setup.sprite_sheet import SpriteSheet


class Explosion:
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.sprite_sheet = SpriteSheet(path.join('assets', 'images', 'spritesheet', 'explosion.png'), (32, 32))
        self.frames = []
        for i in range(explosion_frames):
            if m == 'e':
                img = self.sprite_sheet.get_frame(i * 32, 0, enemy_explosion_radius)
                self.frames.append(img)
            if m == 'p':
                img = self.sprite_sheet.get_frame(i * 32, 0, player_explosion_radius)
                self.frames.append(img)

        self.index = 0
        self.finished = False
        self.frame_time = 0.05
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.frame_time:
            self.index += 1
            self.current_time = 0

            if self.index >= len(self.frames):
                self.finished = True

    def draw(self, window):
        if not self.finished:
            frame = self.frames[self.index]
            rect = frame.get_rect(center=(self.x, self.y))
            window.blit(frame, rect)
