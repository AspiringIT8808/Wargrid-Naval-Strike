"""Win / lose overlay drawn on top of the (frozen) battle screen."""
import pygame

from ui.display import W, screen
from ui.screens.base import Screen
from ui.theme import ACCENT, FONT, HUGE, RED, TEXT
from ui.widgets import text


class GameOverScreen(Screen):
    def on_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.app.goto("menu")
            elif e.key == pygame.K_ESCAPE:
                self.app.quit()

    def draw(self):
        self.app.screens["play"].draw()
        g = self.game

        shade = pygame.Surface((W, 200), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 200))
        screen.blit(shade, (0, 290))

        if g.winner == 0:
            text("CONGRATULATIONS!", (W // 2, 340), HUGE, ACCENT, center=True)
            text("You won the battle!", (W // 2, 395), FONT, TEXT, center=True)
        else:
            text("GAME OVER", (W // 2, 340), HUGE, RED, center=True)
            text("You lost the battle.", (W // 2, 395), FONT, TEXT, center=True)

        text(
            "Press ENTER for the menu or ESC to quit.",
            (W // 2, 445),
            FONT,
            TEXT,
            center=True
        )