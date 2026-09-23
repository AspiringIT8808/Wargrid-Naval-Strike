"""Win / lose overlay drawn on top of the (frozen) battle screen."""
import pygame

from ui.display import W, screen
from ui.screens.base import Screen
from ui.theme import ACCENT, FONT, HUGE, RED, TEXT
from ui.widgets import Button, text


class GameOverScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.btn_stats = Button((W // 2 - 170, 460, 340, 50), "VIEW AFTER-ACTION REPORT")

    def on_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.app.goto("menu")
            elif e.key == pygame.K_ESCAPE:
                self.app.quit()
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_stats.hit(e.pos):
                self.app.goto("stats", return_to="gameover")

    def draw(self):
        self.app.screens["play"].draw()
        g = self.game

        shade = pygame.Surface((W, 250), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 200))
        screen.blit(shade, (0, 290))

        if g.winner == 0:
            text("CONGRATULATIONS!", (W // 2, 340), HUGE, ACCENT, center=True)
            text("You won the battle!", (W // 2, 395), FONT, TEXT, center=True)
        else:
            text("GAME OVER", (W // 2, 340), HUGE, RED, center=True)
            text("You lost the battle.", (W // 2, 395), FONT, TEXT, center=True)

        self.btn_stats.draw()

        text(
            "Press ENTER for the menu or ESC to quit.",
            (W // 2, 525),
            FONT,
            TEXT,
            center=True
        )
