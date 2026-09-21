"""The fleet-status column between the two boards (play screen)."""
import pygame

from ui.display import screen
from ui.layout import STATUS_X
from ui.theme import ACCENT, CYAN, MUTED, RED, SHIP, SMALL, TEXT
from ui.widgets import text


def draw_fleet_status(mine, theirs):
    x, y = STATUS_X, 105
    text("YOUR SHIPS", (x, y), SMALL, ACCENT)
    y += 22
    for ship in mine.ships:
        tag = "  STEALTH" if ship.stealthed else ""
        text(ship.name + tag, (x, y), SMALL, RED if ship.sunk else TEXT)
        for i in range(ship.size):
            r = pygame.Rect(x + i * 18, y + 19, 14, 14)
            pygame.draw.rect(screen, RED if i in ship.hit else SHIP, r)
            if i in ship.shield:
                pygame.draw.rect(screen, CYAN, r, 2)
        y += 44
    y += 8
    text("ENEMY SHIPS", (x, y), SMALL, ACCENT)
    y += 22
    for ship in theirs.ships:
        sunk = ship.sunk
        text(f"{ship.name:<10}{'SUNK' if sunk else 'afloat'}", (x, y), SMALL, RED if sunk else MUTED)
        y += 22
