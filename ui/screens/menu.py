"""Title screen: toggle optional mechanics, pick a mode."""
import pygame

from ui.display import W
from ui.screens.base import Screen
from ui.theme import ACCENT, FONT, HUGE, MUTED, SMALL, TEXT
from ui.widgets import Button, text


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.opt_btns = {k: Button((345 + i * 200, 370, 190, 46)) for i, k in enumerate(app.options)}
        self.diff_btns = {
            d: Button((345 + i * 200, 420, 190, 44))
            for i, d in enumerate(["beginner", "intermediate", "expert"])
        }
        self.btn_ai = Button((345, 480, 290, 60), "PLAY VS COMPUTER")
        self.btn_duo = Button((645, 480, 290, 60), "2 PLAYERS - ONE SCREEN")
        self.btn_codex = Button((1000, 20, 200, 40), "FLEET CODEX")

    def on_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            for key, btn in self.opt_btns.items():
                if btn.hit(e.pos):
                    self.app.options[key] = not self.app.options[key]
            for key, btn in self.diff_btns.items():
                if btn.hit(e.pos):
                    self.app.difficulty = key
            if self.btn_ai.hit(e.pos):
                self.app.new_game("ai")
            elif self.btn_duo.hit(e.pos):
                self.app.new_game("duo")
            elif self.btn_codex.hit(e.pos):
                self.app.goto("codex", return_to="menu")
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.app.quit()

    def draw(self):
        text("WARGRID: NAVAL STRIKE", (W // 2, 100), HUGE, ACCENT, center=True)
        text("TACTICAL EDITION  -  15x15", (W // 2, 150), FONT, MUTED, center=True)
        rules = ["Wargrid: Naval Warfare is a turn-based strategy game for 1 or 2 players OR A.I.",
                 "The goal is to sink the enemy fleet before they sink yours. Strategic placement of ships and use of abilities is key to victory",
                 "You can review and study the fleet in the FLEET CODEX, which is accessible from the main menu.",
                 "A.I difficulty can be adjusted in the main menu, with three options: Beginner, Intermediate, and Expert."]
        for i, line in enumerate(rules):
            text(line, (W // 2, 210 + i * 24), SMALL, TEXT, center=True)
        text("OPTIONAL MECHANICS", (W // 2, 340), SMALL, MUTED, center=True)
        names = {"bomb": "BOMB", "repair": "REPAIR", "shield": "SHIELD"}
        for key, btn in self.opt_btns.items():
            on = self.app.options[key]
            btn.draw(selected=on, label=f"{names[key]}: {'ON' if on else 'OFF'}")
        for key, btn in self.diff_btns.items():
            btn.draw(selected=(self.app.difficulty == key), label=key.upper())
        self.btn_ai.draw()
        self.btn_duo.draw()
        self.btn_codex.draw()
