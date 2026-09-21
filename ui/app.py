"""
THE APP: owns the shared state (options, mode, the Game) and runs the main loop.

Screens: menu -> setup -> (handoff) -> play -> gameover   (see ui/screens/)
Switch screens with app.goto("name"). Don't put drawing or click handling here.
"""
import sys

import pygame

from audio.sound_manager import SoundManager
from rules.game import Game
from ui.display import clock, screen
from ui.screens.gameover import GameOverScreen
from ui.screens.handoff import HandoffScreen
from ui.screens.menu import MenuScreen
from ui.screens.play import PlayScreen
from ui.screens.setup import SetupScreen
from ui.theme import BG
from ui.widgets import MuteButton


class App:
    def __init__(self):
        self.options = {"bomb": True, "repair": True, "shield": True}   # optional mechanics
        self.mode = "ai"                    # "ai" or "duo" (two players, one screen)
        self.game = None
        self.sound_manager = SoundManager()
        self.mute_btn = MuteButton()
        self.screens = {
            "menu": MenuScreen(self),
            "setup": SetupScreen(self),
            "handoff": HandoffScreen(self),
            "play": PlayScreen(self),
            "gameover": GameOverScreen(self),
        }
        self.current = self.screens["menu"]
        self.sound_manager.start_music()

    # ----- navigation -----
    def goto(self, name, **kwargs):
        self.current = self.screens[name]
        self.current.enter(**kwargs)

    def handoff(self, lines, after):
        """Show the curtain screen; call `after()` when the player clicks."""
        self.goto("handoff", lines=lines, after=after)

    def new_game(self, mode):
        """Called from the menu. Creates the Game and starts fleet deployment."""
        self.mode = mode
        self.game = Game(self.options)
        self.game.names = ["Player 1", "Computer" if mode == "ai" else "Player 2"]
        setup = self.screens["setup"]
        setup.index = 0
        if mode == "duo":
            self.handoff(["Player 1: deploy your fleet", "Player 2, look away!"], setup.begin)
        else:
            setup.begin()

    def quit(self):
        self.sound_manager.stop_music()
        pygame.quit()
        sys.exit()

    # ----- main loop -----
    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.quit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if self.mute_btn.hit(e.pos):
                        self.sound_manager.toggle_mute()
                        continue
                self.current.on_event(e)
            self.current.update()
            screen.fill(BG)
            self.current.draw()
            self.mute_btn.draw(muted=self.sound_manager.is_muted)
            pygame.display.flip()
            clock.tick(60)

