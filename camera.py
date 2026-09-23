"""Small, reusable camera for a horizontally scrolling platform world."""
import pygame as pg


class Camera:
    def __init__(self, width, height, world_width):
        self.rect = pg.Rect(0, 0, width, height)
        self.world_width = world_width
  
    def follow(self, target):
        desired = target.centerx - self.rect.width // 2
        self.rect.x += int((desired - self.rect.x) * 0.12)
        self.rect.x = max(0, min(self.rect.x, self.world_width - self.rect.width))

    def apply(self, rect):
        return rect.move(-self.rect.x, -self.rect.y)
