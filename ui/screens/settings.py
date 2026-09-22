"""In-game ESC settings screen."""

import pygame

from settings.settings import SETTINGS
from ui.display import W, screen
from ui.screens.base import Screen
from ui.theme import ACCENT, BIG, FONT, MUTED, TEXT
from ui.widgets import Button, text


class SettingsScreen(Screen):

    def __init__(self, app):
        super().__init__(app)

        self.return_to = "play"

        # -------------------------
        # Centered button layout
        # -------------------------

        button_w = 340
        button_h = 60
        button_gap = 20

        center_x = W // 2
        button_x = center_x - (button_w // 2)

        self.back_btn = Button(
            (button_x, 245, button_w, button_h)
        )

        self.restart_btn = Button(
            (button_x, 245 + button_h + button_gap, button_w, button_h)
        )

        self.menu_btn = Button(
            (button_x, 245 + (button_h + button_gap) * 2, button_w, button_h)
        )

    # -------------------------
    # Screen control
    # -------------------------

    def enter(self, return_to="play"):
        self.return_to = return_to

    def close(self):
        self.app.goto(self.return_to)

    def restart_level(self):
        self.app.screens["play"].restart_level()

    # -------------------------
    # Input
    # -------------------------

    def on_event(self, e):

        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                self.close()

            elif e.key == pygame.K_1:
                self.close()

            elif e.key == pygame.K_2:
                self.restart_level()

            elif e.key == pygame.K_3:
                self.app.goto("menu")

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

            if self.back_btn.hit(e.pos):
                self.close()

            elif self.restart_btn.hit(e.pos):
                self.restart_level()

            elif self.menu_btn.hit(e.pos):
                self.app.goto("menu")

    # -------------------------
    # Drawing
    # -------------------------

    def draw(self):

        # Draw the game underneath the settings overlay.
        self.app.screens[self.return_to].draw()

        # Dark overlay.
        overlay = pygame.Surface((W, 800), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, SETTINGS.overlay_alpha))
        screen.blit(overlay, (0, 0))

        # -------------------------
        # Title
        # -------------------------

        text(
            SETTINGS.title,
            (W // 2, 145),
            BIG,
            ACCENT,
            center=True
        )

        # -------------------------
        # Buttons
        # -------------------------

        self.back_btn.draw(
            True,
            False,
            None,
            SETTINGS.back_label
        )

        self.restart_btn.draw(
            True,
            False,
            None,
            SETTINGS.restart_label
        )

        self.menu_btn.draw(
            True,
            False,
            None,
            SETTINGS.menu_label
        )

        # -------------------------
        # Bottom hints
        # -------------------------

        text(
            SETTINGS.esc_hint,
            (W // 2, 490),
            FONT,
            MUTED,
            center=True
        )

        text(
            SETTINGS.controls_label,
            (W // 2, 525),
            FONT,
            TEXT,
            center=True
        )