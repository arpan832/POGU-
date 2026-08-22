"""Loading and preparing visual game assets."""
from dataclasses import dataclass
import pygame as pg

from game_settings import BASE_DIR


@dataclass
class Assets:
    sky: pg.Surface
    ground: pg.Surface
    player_stand: pg.Surface
    intro_player_rect: pg.Rect
    intro_surface: pg.Surface
    intro_rect: pg.Rect
    game_name_surface: pg.Surface
    game_name_rect: pg.Rect
    apple: pg.Surface
    apple_rect: pg.Rect
    game_over_surface: pg.Surface
    game_over_rect: pg.Rect
    restart_surface: pg.Surface
    restart_rect: pg.Rect
    snail_paths: list


def load_assets(font):
    graphics = BASE_DIR / "Graphics"
    load = lambda name: pg.image.load(str(graphics / name)).convert_alpha()
    player_stand = pg.transform.scale(load("main11.png"), (250,250))
    apple = pg.image.load(str(BASE_DIR / "sprites" / "apple.png")).convert_alpha()
    apple = pg.transform.flip(pg.transform.scale_by(apple, 5), True, False)
    intro_surface = font.render("press 3 to start", False, (65, 105, 225))
    game_name_surface = font.render("POGU", False, (65, 105, 225))
    game_over_surface = font.render("GAME OVER", False, "Black")
    restart_surface = font.render("press 1 to restart", False, "Black")
    return Assets(
        sky=load("sky.png"), ground=load("platform2.png"), player_stand=player_stand,
        intro_player_rect=player_stand.get_rect(center=(600, 250)),
        intro_surface=intro_surface, intro_rect=intro_surface.get_rect(center=(600, 400)),
        game_name_surface=game_name_surface, game_name_rect=game_name_surface.get_rect(center=(600, 100)),
        apple=apple, apple_rect=apple.get_rect(center=(200, 200)),
        game_over_surface=game_over_surface, game_over_rect=game_over_surface.get_rect(center=(550, 100)),
        restart_surface=restart_surface, restart_rect=restart_surface.get_rect(midbottom=(550, 150)),
        snail_paths=[graphics / "snailWalk1.png", graphics / "snailWalk2.png"],
    )

