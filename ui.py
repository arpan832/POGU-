"""HUD and score rendering."""
import pygame as pg


def draw_score(screen, font, start_time):
    elapsed = pg.time.get_ticks() - start_time
    score = int(elapsed / 100)
    surface = font.render(f"score {score}", False, (64, 64, 64))
    rectangle = surface.get_rect(center=(550, 50))
    screen.blit(surface, rectangle)
    pg.draw.rect(screen, "white", rectangle, 2)
    return score

