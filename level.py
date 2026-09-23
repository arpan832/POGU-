"""Stage data and world objects for POGU."""
from dataclasses import dataclass
import pygame as pg

from game_settings import GROUND_Y, WORLD_WIDTH


@dataclass
class Coin:
    rect: pg.Rect
    taken: bool = False


@dataclass
class Goal:
    rect: pg.Rect


class Stage:
    NAMES = ("Meadow Run", "Twilight Woods", "Castle Approach")
    SKY = ((151, 220, 242), (107, 142, 196), (76, 83, 142))
    GROUND = ((76, 164, 71), (72, 124, 82), (96, 90, 120))

    def __init__(self, number, assets):
        self.number = number
        self.name = self.NAMES[number - 1]
        self.sky_color = self.SKY[number - 1]
        self.ground_color = self.GROUND[number - 1]
        self.solids = []
        self.coins = []
        self.enemies = []
        self.goal = Goal(pg.Rect(WORLD_WIDTH - 180, 320, 48, 180))
        self._build(assets)

    def _build(self, assets):
        # A continuous floor keeps the first stage friendly; raised platforms
        # create the rhythm and make the camera movement meaningful.
        self.solids.append(pg.Rect(0, GROUND_Y, WORLD_WIDTH, 100))
        patterns = {
            1: [(650, 410, 180), (1050, 340, 180), (1450, 430, 220),
                (1900, 360, 210), (2400, 300, 190), (2860, 410, 220),
                (3330, 350, 190), (3800, 275, 210), (4250, 390, 220)],
            2: [(520, 360, 180), (900, 270, 170), (1320, 400, 180),
                (1750, 310, 210), (2210, 235, 180), (2640, 390, 180),
                (3100, 300, 200), (3550, 210, 190), (4020, 360, 220)],
            3: [(500, 400, 180), (850, 320, 160), (1200, 240, 160),
                (1600, 380, 210), (2050, 290, 180), (2500, 200, 180),
                (2920, 360, 200), (3400, 270, 180), (3850, 180, 180),
                (4250, 340, 220)],
        }
        for x, y, width in patterns[self.number]:
            self.solids.append(pg.Rect(x, y, width, 28))
            for coin_x in range(x + 35, x + width - 15, 45):
                self.coins.append(Coin(pg.Rect(coin_x, y - 42, 22, 22)))

        # Ground-level coin arcs and enemies are placed in world coordinates.
        for x in range(300, WORLD_WIDTH - 300, 420):
            self.coins.append(Coin(pg.Rect(x, 430, 22, 22)))
        enemy_count = 2 + self.number
        for index in range(enemy_count):
            x = 760 + index * 760 + (self.number - 1) * 90
            self.enemies.append(Enemy(x, GROUND_Y - 42, assets.snail_paths))

    def reset(self, assets):
        self.__init__(self.number, assets)

    def draw(self, screen, camera, assets):
        screen.fill(self.sky_color)
        # Simple parallax bands make the scrolling visible even on systems
        # where the optional background artwork is unavailable.
        offset = int(camera.rect.x * 0.18) % 260
        for x in range(-260 - offset, screen.get_width() + 260, 260):
            pg.draw.polygon(screen, tuple(max(0, c - 25) for c in self.sky_color),
                            [(x, 420), (x + 130, 300), (x + 260, 420)])
        for solid in self.solids:
            draw_rect = camera.apply(solid)
            if draw_rect.bottom < 0 or draw_rect.top > screen.get_height():
                continue
            pg.draw.rect(screen, self.ground_color, draw_rect)
            pg.draw.line(screen, (198, 232, 113), draw_rect.topleft,
                         draw_rect.topright, 5)
        for coin in self.coins:
            if not coin.taken:
                r = camera.apply(coin.rect)
                pg.draw.circle(screen, (255, 215, 55), r.center, r.width // 2)
                pg.draw.circle(screen, (255, 244, 150), r.center, r.width // 2, 2)
        goal = camera.apply(self.goal.rect)
        pg.draw.rect(screen, (230, 230, 230), (goal.x + 8, goal.y, 6, goal.height))
        pg.draw.polygon(screen, (55, 208, 102), [(goal.x + 14, goal.y + 8),
                                                  (goal.x + 52, goal.y + 24),
                                                  (goal.x + 14, goal.y + 40)])


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, paths):
        super().__init__()
        self.frames = [pg.image.load(str(path)).convert_alpha() for path in paths]
        self.frames = [pg.transform.scale_by(frame, 2.5) for frame in self.frames]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.direction = -1
        self.index = 0

    def update(self, solids):
        self.rect.x += self.direction * (1.2 + len(solids) * 0.0)
        if self.rect.x < self.start_x - 100 or self.rect.x > self.start_x + 100:
            self.direction *= -1
        self.index = (self.index + 0.12) % len(self.frames)
        self.image = self.frames[int(self.index)]
