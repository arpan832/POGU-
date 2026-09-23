"""POGU: a small three-stage side-scrolling platform adventure."""
import asyncio
import pygame as pg

from assets import load_assets
from audio import load_audio, start_music, stop_music
from camera import Camera
from game_settings import BASE_DIR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, STAGE_COUNT, WORLD_WIDTH
from level import Stage
from player import Player


def draw_text(screen, font, text, position, color=(255, 255, 255), center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=position) if center else surface.get_rect(topleft=position)
    screen.blit(surface, rect)


def draw_hud(screen, font, stage, score, lives, camera):
    panel = pg.Surface((SCREEN_WIDTH, 58), pg.SRCALPHA)
    panel.fill((16, 25, 40, 190))
    screen.blit(panel, (0, 0))
    collected = len(stage.coins) - sum(not coin.taken for coin in stage.coins)
    draw_text(screen, font, f"STAGE {stage.number}/{STAGE_COUNT}  {stage.name}", (20, 14))
    draw_text(screen, font, f"COINS {collected:02d}/{len(stage.coins):02d}", (430, 14))
    draw_text(screen, font, f"LIVES {'♥' * lives}", (930, 14), (255, 210, 90))
    bar = pg.Rect(20, 70, 250, 10)
    pg.draw.rect(screen, (25, 35, 50), bar, border_radius=5)
    progress = min(1, max(0, camera.rect.centerx / WORLD_WIDTH))
    pg.draw.rect(screen, (255, 213, 77), (bar.x, bar.y, int(bar.width * progress), bar.height), border_radius=5)


def draw_panel(screen, font, title, lines, color=(18, 26, 42, 230)):
    panel = pg.Surface((720, 330), pg.SRCALPHA)
    panel.fill(color)
    screen.blit(panel, panel.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    draw_text(screen, font, title, (SCREEN_WIDTH // 2, 185), (255, 220, 100), True)
    for index, line in enumerate(lines):
        draw_text(screen, font, line, (SCREEN_WIDTH // 2, 250 + index * 45), (245, 245, 245), True)


def reset_stage(stage_number, assets, player):
    stage = Stage(stage_number, assets)
    player.reset_position()
    return stage


async def main():
    pg.init()
    try:
        pg.mixer.init()
    except pg.error:
        pass
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("POGU - Meadow Quest")
    font_path = BASE_DIR / "arcadeclassic" / "ARCADECLASSIC.TTF"
    font = pg.font.Font(str(font_path), 25)
    title_font = pg.font.Font(str(font_path), 48)
    audio = load_audio()
    assets = load_assets(font)
    player = Player(BASE_DIR / "Graphics" / "main11.png", audio.get("startup"))
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH)
    stage_number, score, lives = 1, 0, 3
    stage = reset_stage(stage_number, assets, player)
    state, message_timer = "title", 0
    start_music(audio)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                stop_music(audio, play_game_over=False)
                return
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_RETURN, pg.K_SPACE) and state in ("title", "game_over", "victory"):
                    stage_number, score, lives = 1, 0, 3
                    stage = reset_stage(stage_number, assets, player)
                    state = "playing"
                    start_music(audio)
                elif event.key == pg.K_p and state in ("playing", "paused"):
                    state = "paused" if state == "playing" else "playing"
                elif event.key == pg.K_r and state in ("playing", "paused"):
                    stage = reset_stage(stage_number, assets, player)
                    state = "playing"

        if state == "playing":
            player.update(pg.key.get_pressed(), stage.solids)
            for enemy in stage.enemies:
                enemy.update(stage.solids)
            for coin in stage.coins:
                if not coin.taken and player.rect.colliderect(coin.rect):
                    coin.taken = True
                    score += 100
                    if audio.get("startup"):
                        audio["startup"].play()
            hit_enemy = next((e for e in stage.enemies if player.rect.colliderect(e.rect)), None)
            if hit_enemy:
                if player.gravity > 0 and player.rect.bottom - hit_enemy.rect.top < 25:
                    player.gravity = -10
                    stage.enemies.remove(hit_enemy)
                    score += 250
                else:
                    lives -= 1
                    if lives <= 0:
                        state = "game_over"
                        stop_music(audio)
                    else:
                        player.reset_position()
                        message_timer = pg.time.get_ticks() + 900
            if state == "playing" and player.rect.colliderect(stage.goal.rect):
                score += 500
                if stage_number < STAGE_COUNT:
                    stage_number += 1
                    stage = reset_stage(stage_number, assets, player)
                    message_timer = pg.time.get_ticks() + 1400
                else:
                    state = "victory"
                    stop_music(audio, play_game_over=False)
            camera.follow(player.rect)

        stage.draw(screen, camera, assets)
        for enemy in stage.enemies:
            screen.blit(enemy.image, camera.apply(enemy.rect))
        screen.blit(player.image, camera.apply(player.rect))
        if state == "playing":
            draw_hud(screen, font, stage, score, lives, camera)
            if message_timer > pg.time.get_ticks():
                draw_text(screen, title_font, f"STAGE {stage_number}: {stage.name}",
                          (SCREEN_WIDTH // 2, 150), (255, 235, 130), True)
        elif state == "title":
            draw_panel(screen, title_font, "POGU", ["ENTER / SPACE  -  START ADVENTURE",
                                                      "A D / ARROWS - MOVE     SPACE - JUMP",
                                                      "P - PAUSE     R - RESTART STAGE"])
        elif state == "paused":
            draw_panel(screen, title_font, "PAUSED", ["P - RESUME", "R - RESTART STAGE"])
        elif state == "game_over":
            draw_panel(screen, title_font, "GAME OVER", [f"FINAL SCORE: {score}", "ENTER / SPACE - TRY AGAIN"])
        elif state == "victory":
            draw_panel(screen, title_font, "ADVENTURE COMPLETE", [f"FINAL SCORE: {score}", "ENTER / SPACE - PLAY AGAIN"])
        pg.display.flip()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
