"""
FLEET CODEX - ship & mechanic reference, browsed one entry at a time like a
field manual. Pure display: reads SHIP_SPECS for stats and ui/lore.py for
flavor text. Changes nothing in rules/.
"""
import pygame

from rules.config import SHIP_SPECS
from ui.display import W, screen
from ui.lore import MECHANIC_LORE, SHIP_LORE
from ui.screens.base import Screen
from ui.theme import (ACCENT, BIG, FAINT, FONT, GOLD, HUGE, LABEL, MUTED,
                       SHIP, SMALL, TEXT, panel)
from ui.widgets import Button, text

ENTRIES = (
    [dict(kind="ship", **s) for s in SHIP_SPECS] +
    [dict(kind="mechanic", name=n) for n in ("Bomb", "Repair", "Shield")]
)


class CodexScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.index = 0
        self.return_to = "menu"
        self.btn_prev = Button((80, 700, 140, 46), "< PREV")
        self.btn_next = Button((W - 220, 700, 140, 46), "NEXT >")
        self.btn_back = Button((W // 2 - 90, 700, 180, 46), "BACK")

    def enter(self, return_to="menu"):
        self.return_to = return_to
        self.index = 0

    def on_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.app.goto(self.return_to)
            elif e.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(ENTRIES)
            elif e.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(ENTRIES)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_prev.hit(e.pos):
                self.index = (self.index - 1) % len(ENTRIES)
            elif self.btn_next.hit(e.pos):
                self.index = (self.index + 1) % len(ENTRIES)
            elif self.btn_back.hit(e.pos):
                self.app.goto(self.return_to)

    def draw(self):
        entry = ENTRIES[self.index]
        text("FLEET CODEX", (W // 2, 50), HUGE, ACCENT, center=True)
        text("FIELD DOSSIER  -  KNOW YOUR HULLS", (W // 2, 95), SMALL, MUTED, center=True)

        card = pygame.Rect(W // 2 - 340, 140, 680, 530)
        panel(screen, card, fill=(20, 28, 38), border=ACCENT, border_w=2, radius=14)

        if entry["kind"] == "ship":
            self.draw_ship(entry, card)
        else:
            self.draw_mechanic(entry, card)

        text(f"{self.index + 1} / {len(ENTRIES)}", (W // 2, card.bottom + 24), SMALL, MUTED, center=True)

        self.btn_prev.draw()
        self.btn_next.draw()
        self.btn_back.draw()

    def draw_ship(self, entry, card):
        lore = SHIP_LORE.get(entry["name"], {})
        x, y = card.x + 40, card.y + 34

        text(entry["name"].upper(), (x, y), BIG, TEXT)
        text(lore.get("class_tag", ""), (x, y + 34), LABEL, GOLD)

        # Silhouette: size blocks, echoing the ship art on the battle boards.
        sx, sy = card.right - 260, y
        for i in range(entry["size"]):
            r = pygame.Rect(sx + i * 34, sy, 28, 28)
            pygame.draw.rect(screen, SHIP, r, border_radius=4)
            pygame.draw.rect(screen, TEXT, r, 1, border_radius=4)
        text(f"SIZE {entry['size']}", (sx, sy + 40), SMALL, MUTED)

        y += 80
        pygame.draw.line(screen, FAINT, (card.x + 30, y), (card.right - 30, y), 1)
        y += 24

        text("ABILITY", (x, y), LABEL, ACCENT)
        y += 22
        text(entry["label"], (x, y), FONT, TEXT)
        y += 30
        uses = "Unlimited uses" if entry["uses"] is None else f"{entry['uses']} use(s) per battle"
        text(uses, (x, y), SMALL, MUTED)
        y += 44

        text("REAL-WORLD NOTE", (x, y), LABEL, ACCENT)
        y += 22
        y = self.wrap(lore.get("blurb", ""), x, y, card.width - 80)
        y += 18

        text("TACTICAL TIP", (x, y), LABEL, GOLD)
        y += 22
        self.wrap(lore.get("tip", ""), x, y, card.width - 80)

    def draw_mechanic(self, entry, card):
        lore = MECHANIC_LORE.get(entry["name"], {})
        x, y = card.x + 40, card.y + 34
        text(entry["name"].upper(), (x, y), BIG, TEXT)
        text(lore.get("class_tag", ""), (x, y + 34), LABEL, GOLD)
        y += 90
        pygame.draw.line(screen, FAINT, (card.x + 30, y), (card.right - 30, y), 1)
        y += 24
        text("OPTIONAL MECHANIC", (x, y), LABEL, ACCENT)
        y += 22
        y = self.wrap(lore.get("blurb", ""), x, y, card.width - 80)
        y += 18
        text("TACTICAL TIP", (x, y), LABEL, GOLD)
        y += 22
        self.wrap(lore.get("tip", ""), x, y, card.width - 80)

    @staticmethod
    def wrap(s, x, y, max_w, font=FONT, color=TEXT, line_h=24):
        """Minimal word-wrap so the dossier text fits inside the card."""
        words, line = s.split(), ""
        for w in words:
            trial = f"{line} {w}".strip()
            if font.size(trial)[0] > max_w and line:
                text(line, (x, y), font, color)
                y += line_h
                line = w
            else:
                line = trial
        if line:
            text(line, (x, y), font, color)
            y += line_h
        return y
