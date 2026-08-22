"""Snail enemy movement and animation mechanics."""

import pygame as pg

from game_settings import GROUND_Y, SCREEN_WIDTH, SNAIL_SPEED


class Snail:
    def __init__(self, image_paths, scale=3):
        self.walk = []
        for path in image_paths:
            image = pg.image.load(str(path)).convert_alpha()
            size = (int(image.get_width() * scale), int(image.get_height() * scale))
            self.walk.append(pg.transform.scale(image, size))
        self.index = 0
        self.image = self.walk[0]
        self.rect = self.image.get_rect(midbottom=(900, GROUND_Y))

    def update(self):
        self.rect.x -= SNAIL_SPEED
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        self.index = (self.index + 0.1) % len(self.walk)
        self.image = self.walk[int(self.index)]

    def reset(self):
        self.rect.left = SCREEN_WIDTH

