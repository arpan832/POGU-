"""POGU entry point and game-state loop."""
from sys import exit

import pygame as pg

from assets import load_assets
from audio import load_audio, start_music, stop_music
from game_settings import BASE_DIR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from snail import Snail
from ui import draw_score


def main():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("POGU")
    clock = pg.time.Clock()
    font = pg.font.Font(str(BASE_DIR / "arcadeclassic" / "ARCADECLASSIC.TTF"), 30)

    audio = load_audio()
    assets = load_assets(font)
    player = Player(BASE_DIR / "Graphics" / "main11.png", audio["startup"])
    player_group = pg.sprite.GroupSingle(player)
    snail = Snail(assets.snail_paths)

    start_time = 0
    intro_panel = True
    game_active = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 and not game_active:
                    snail.reset()
                    player.reset_position()
                    start_time = pg.time.get_ticks()
                    start_music(audio)
                    game_active = True
                    intro_panel = False

                if event.key == pg.K_3 and intro_panel:
                    intro_panel = False
                    game_active = True
                    start_time = pg.time.get_ticks()
                    if audio["startup"]:
                        audio["startup"].play()
                    start_music(audio)

        if intro_panel:
            screen.fill("Light Blue")
            screen.blit(assets.player_stand, assets.intro_player_rect)
            screen.blit(assets.intro_surface, assets.intro_rect)
            screen.blit(assets.game_name_surface, assets.game_name_rect)
            screen.blit(assets.apple, assets.apple_rect)
        elif game_active:
            screen.blit(assets.sky, (0, 0))
            screen.blit(assets.ground, (0, 500))
            snail.update()
            screen.blit(snail.image, snail.rect)
            draw_score(screen, font, start_time)
            player_group.update()
            player_group.draw(screen)

            if player.rect.colliderect(snail.rect):
                game_active = False
                stop_music(audio)
        else:
            screen.fill("Red")
            screen.blit(assets.game_over_surface, assets.game_over_rect)
            screen.blit(assets.restart_surface, assets.restart_rect)
            
        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
