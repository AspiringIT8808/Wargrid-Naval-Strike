"""Background music manager."""
import os
import pygame

MUSIC_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "bg_music .mp3")


class MusicPlayer:
    def __init__(self):
        self.muted = False

    def start(self):
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def toggle_mute(self):
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0.0 if self.muted else 1.0)
        return self.muted
