"""Central audio manager for WARGRID: Naval Strike."""
from audio.music import MusicPlayer


class SoundManager:
    def __init__(self):
        self.music = MusicPlayer()

    @property
    def is_muted(self):
        return self.music.muted

    def start_music(self):
        self.music.start()

    def stop_music(self):
        self.music.stop()

    def toggle_mute(self):
        return self.music.toggle_mute()
