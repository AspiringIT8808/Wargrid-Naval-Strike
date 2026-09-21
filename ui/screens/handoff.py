"""Curtain shown between hot-seat players so nobody sees the other's board."""
import pygame

from ui.display import H, W
from ui.screens.base import Screen
from ui.theme import ACCENT, BIG, FONT, MUTED, TEXT
from ui.widgets import text


class HandoffScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.lines = []
        self.after = None

    def enter(self, lines, after):
        self.lines = lines
        self.after = after                  # function to call when the player clicks

    def on_event(self, e):
        if (e.type == pygame.MOUSEBUTTONDOWN and e.button == 1) or \
           (e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_RETURN)):
            self.after()

    def draw(self):
        for i, line in enumerate(self.lines):
            text(line, (W // 2, 260 + i * 44), BIG if i == 0 else FONT, ACCENT if i == 0 else TEXT, center=True)
        text("Click or press SPACE to continue", (W // 2, H - 90), FONT, MUTED, center=True)
