"""Player sprite and movement mechanics."""
import pygame as pg

from game_settings import GRAVITY, GROUND_Y, JUMP_SPEED, PLAYER_SPEED


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
        self.rect = self.image.get_rect(midbottom=(180, GROUND_Y))
        self.gravity = 0
        self.speed = PLAYER_SPEED
        self.startup_sound = startup_sound
        self.facing_right = True
        self.on_ground = False

    def player_input(self, keys):
        if (keys[pg.K_SPACE] or keys[pg.K_w] or keys[pg.K_UP]) and self.on_ground:
            self.gravity = JUMP_SPEED
            self.on_ground = False
            if self.startup_sound:
                self.startup_sound.play()
        dx = (keys[pg.K_d] or keys[pg.K_RIGHT]) - (keys[pg.K_a] or keys[pg.K_LEFT])
        self.rect.x += dx * self.speed
        if dx:
            self.facing_right = dx > 0

    def apply_gravity(self, solids):
        self.gravity += GRAVITY
        self.rect.y += self.gravity
        self.on_ground = False
        for solid in solids:
            if self.rect.colliderect(solid) and self.gravity >= 0:
                self.rect.bottom = solid.top
                self.gravity = 0
                self.on_ground = True
                break

    def animate(self):
        if self.rect.bottom < GROUND_Y:
            self.image = self.player_jump
        else:
            self.player_index = (self.player_index + 0.1) % len(self.player_walk)
            self.image = self.player_walk[int(self.player_index)]
        if not self.facing_right:
            self.image = pg.transform.flip(self.image, True, False)

    def reset_position(self):
        self.rect.midbottom = (180, GROUND_Y)
        self.gravity = 0
        self.on_ground = False

    def update(self, keys, solids):
        self.player_input(keys)
        self.apply_gravity(solids)
        self.animate()
