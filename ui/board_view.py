"""Drawing a board: the grid, ships, markers, previews. Also pixel <-> cell conversion."""
import pygame

from rules.config import GRID
from ui.display import screen
from ui.layout import BOARD_PX, CELL
from ui.theme import (BG, CYAN, GRID_C, MUTED, ORANGE, RED, SCAN_SHIP, SCAN_WATER, SHIP, SHIP_HIT,
                      SHIP_STEALTH, SHIP_SUNK, SMALL, WATER, WHITE, YELLOW)
from ui.widgets import text


def cell_rect(ox, oy, cell):
    return pygame.Rect(ox + cell[1] * CELL, oy + cell[0] * CELL, CELL, CELL)


def cell_at(pos, ox, oy):
    """Pixel position -> (row, col), or None if it isn't over the board at (ox, oy)."""
    c, r = (pos[0] - ox) // CELL, (pos[1] - oy) // CELL
    return (r, c) if 0 <= r < GRID and 0 <= c < GRID else None


def highlight(cells, ox, oy, color):
    """Translucent overlay on some cells (hover previews). color is RGBA."""
    tile = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
    tile.fill(color)
    for cell in cells:
        screen.blit(tile, cell_rect(ox, oy, cell).topleft)


def draw_grid(ox, oy):
    pygame.draw.rect(screen, WATER, (ox, oy, BOARD_PX, BOARD_PX))
    for i in range(GRID + 1):
        pygame.draw.line(screen, GRID_C, (ox + i * CELL, oy), (ox + i * CELL, oy + BOARD_PX))
        pygame.draw.line(screen, GRID_C, (ox, oy + i * CELL), (ox + BOARD_PX, oy + i * CELL))
    for i in range(GRID):
        text(chr(65 + i), (ox + i * CELL + CELL // 2, oy - 12), SMALL, MUTED, center=True)
        text(str(i + 1), (ox - 14, oy + i * CELL + CELL // 2), SMALL, MUTED, center=True)


def draw_marker(kind, rect):
    cx, cy = rect.center
    if kind == "hit":
        pygame.draw.circle(screen, RED, (cx, cy), 10)
        pygame.draw.line(screen, WHITE, (cx - 6, cy - 6), (cx + 6, cy + 6), 2)
        pygame.draw.line(screen, WHITE, (cx + 6, cy - 6), (cx - 6, cy + 6), 2)
    elif kind == "miss":
        pygame.draw.circle(screen, MUTED, (cx, cy), 3)
    elif kind == "blocked":
        pygame.draw.circle(screen, CYAN, (cx, cy), 10, 3)
    elif kind == "bomb":
        pygame.draw.circle(screen, ORANGE, (cx, cy), 11)
        text("B", (cx, cy), SMALL, BG, center=True)


def draw_own_board(board, ox, oy):
    """Everything is visible: your ships, damage, shields, bomb and the enemy's misses."""
    draw_grid(ox, oy)
    for ship in board.ships:
        for i, cell in enumerate(ship.cells):
            rect = cell_rect(ox, oy, cell).inflate(-4, -4)
            color = SHIP_HIT if i in ship.hit else (SHIP_STEALTH if ship.stealthed else SHIP)
            if ship.sunk:
                color = SHIP_SUNK
            pygame.draw.rect(screen, color, rect, border_radius=3)
            if i in ship.hit:
                pygame.draw.line(screen, WHITE, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, WHITE, rect.topright, rect.bottomleft, 2)
            elif i == 0:
                text(ship.name[0], rect.center, SMALL, BG, center=True)
            if i in ship.shield:
                pygame.draw.rect(screen, CYAN, rect, 3, border_radius=3)
    if board.bomb:
        r = cell_rect(ox, oy, board.bomb)
        pygame.draw.polygon(screen, ORANGE, [(r.centerx, r.top + 5), (r.right - 5, r.centery),
                                             (r.centerx, r.bottom - 5), (r.left + 5, r.centery)], 2)
    for cell, kind in board.shots.items():
        if kind != "hit":                       # hits already show as damaged ship cells
            draw_marker(kind, cell_rect(ox, oy, cell))


def draw_enemy_board(board, ox, oy, reveal=False):
    """Only what you have learned: shots, scans. (reveal=True after the game ends.)"""
    draw_grid(ox, oy)
    for cell, occupied in board.scanned.items():
        rect = cell_rect(ox, oy, cell)
        pygame.draw.rect(screen, SCAN_SHIP if occupied else SCAN_WATER, rect.inflate(-2, -2))
        if occupied and cell not in board.shots:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(0, 0, 8, 8).move(rect.centerx - 4, rect.centery - 4))
    if reveal:
        for ship in board.ships:
            for cell in ship.cells:
                pygame.draw.rect(screen, SHIP, cell_rect(ox, oy, cell).inflate(-6, -6), 2, border_radius=3)
    for cell, kind in board.shots.items():
        draw_marker(kind, cell_rect(ox, oy, cell))
