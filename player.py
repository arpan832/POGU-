"""Player sprite and movement mechanics."""
import pygame as pg

from game_settings import GROUND_Y, PLAYER_SPEED, SCREEN_WIDTH


class Player(pg.sprite.Sprite):
    def __init__(self, image_path, startup_sound=None):
        super().__init__()
        image = pg.image.load(str(image_path)).convert_alpha()
        image = pg.transform.scale(image, (110, 110))
        self.player_walk = [image, image.copy()]
        self.player_jump = image.copy()
        self.player_flipped = pg.transform.flip(image, True, False)
        self.player_index = 0
        self.image = self.player_walk[0]
        self.rect = self.image.get_rect(midbottom=(200, GROUND_Y))
        self.gravity = 0
        self.speed = PLAYER_SPEED
        self.startup_sound = startup_sound

    def player_input(self):
        keys = pg.key.get_pressed()
        if (keys[pg.K_SPACE] or keys[pg.K_w]) and self.rect.bottom >= GROUND_Y:
            self.gravity = -25 if keys[pg.K_SPACE] else -20
            if self.startup_sound:
                self.startup_sound.play()
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.gravity = 0

    def animate(self):
        if self.rect.bottom < GROUND_Y:
            self.image = self.player_jump
        else:
            self.player_index = (self.player_index + 0.1) % len(self.player_walk)
            self.image = self.player_walk[int(self.player_index)]

    def reset_position(self):
        self.rect.midbottom = (200, GROUND_Y)
        self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

