"""
AFTER-ACTION REPORT - post-battle statistics, reachable from the Game Over
screen. Reads Game.stats (rules/stats.py) and only ever draws; it never
touches game state. Works the same for Player vs Computer and 2-player.
"""
import pygame

from ui.display import W, screen
from ui.screens.base import Screen
from ui.theme import ACCENT, BIG, FAINT, FONT, GOLD, HUGE, LABEL, MUTED, TEXT, panel
from ui.widgets import Button, text


class StatsScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.return_to = "gameover"
        self.btn_menu = Button((W // 2 - 320, 715, 260, 50), "MAIN MENU")
        self.btn_back = Button((W // 2 + 60, 715, 260, 50), "BACK")

    def enter(self, return_to="gameover"):
        self.return_to = return_to

    def on_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.app.goto(self.return_to)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.btn_menu.hit(e.pos):
                self.app.goto("menu")
            elif self.btn_back.hit(e.pos):
                self.app.goto(self.return_to)

    def draw(self):
        g = self.game
        stats = getattr(g, "stats", None)

        text("AFTER-ACTION REPORT", (W // 2, 46), HUGE, ACCENT, center=True)

        if stats is None:
            text("No battle data recorded.", (W // 2, 140), FONT, MUTED, center=True)
            self.btn_menu.draw()
            self.btn_back.draw()
            return

        mins, secs = divmod(int(stats.duration_seconds), 60)
        winner = g.names[g.winner].upper() if g.winner is not None else "N/A"
        summary = f"{stats.turns} turns  -  {mins}m {secs:02d}s  -  WINNER: {winner}"
        text(summary, (W // 2, 90), FONT, GOLD, center=True)

        col_w, gap = 560, 40
        left_x = W // 2 - col_w - gap // 2
        right_x = W // 2 + gap // 2

        self.draw_column(stats.players[0], pygame.Rect(left_x, 130, col_w, 560), g.winner == 0)
        self.draw_column(stats.players[1], pygame.Rect(right_x, 130, col_w, 560), g.winner == 1)

        self.btn_menu.draw()
        self.btn_back.draw()

    def draw_column(self, p, rect, won):
        panel(screen, rect, fill=(18, 25, 35), border=GOLD if won else FAINT,
              border_w=3 if won else 1, radius=12)

        x, y = rect.x + 30, rect.y + 26
        title = p.name.upper() + ("  -  VICTOR" if won else "")
        text(title, (x, y), BIG, GOLD if won else TEXT)
        y += 46

        rows = [
            ("Shots fired", str(p.shots)),
            ("Hits", str(p.hits)),
            ("Misses", str(p.misses)),
            ("Accuracy", f"{p.accuracy:.0f}%"),
            ("Shots shield-blocked", str(p.blocked)),
            ("Enemy ships sunk", str(p.ships_sunk)),
            ("Own hull segments lost", str(p.damage_taken)),
            ("Repairs used", str(p.repairs_used)),
            ("Shields raised", str(p.shields_used)),
            ("Bombs detonated", str(p.bombs_triggered)),
        ]
        for label, value in rows:
            text(label, (x, y), FONT, MUTED)
            vw = FONT.size(value)[0]
            text(value, (rect.right - 30 - vw, y), FONT, TEXT)
            y += 27

        y += 8
        pygame.draw.line(screen, FAINT, (x, y), (rect.right - 30, y), 1)
        y += 18
        text("ABILITIES USED", (x, y), LABEL, ACCENT)
        y += 24
        if p.abilities_used:
            for label, count in p.abilities_used.items():
                text(f"{label}  x{count}", (x, y), FONT, TEXT)
                y += 24
        else:
            text("None", (x, y), FONT, MUTED)
