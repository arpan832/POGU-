"""Game sound and music loading."""
import pygame as pg

from game_settings import BASE_DIR


def load_audio():
    try:
        return {
            "startup": pg.mixer.Sound(str(BASE_DIR / "realstartup.wav")),
            "game_over": pg.mixer.Sound(str(BASE_DIR / "gameover.wav")),
            "music": BASE_DIR / "background.mp3",
        }
    except (FileNotFoundError, pg.error) as error:
        print(f"Audio files missing or unable to load: {error}")
        return {"startup": None, "game_over": None, "music": None}


def start_music(audio):
    if audio["music"]:
        try:
            pg.mixer.music.load(str(audio["music"]))
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(0.3)
        except pg.error:
            pass


def stop_music(audio):
    pg.mixer.music.stop()
    if audio["game_over"]:
        audio["game_over"].play()

