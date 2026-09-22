"""Drawing a board: the grid, ships, markers, previews. Also pixel <-> cell conversion."""
import pygame

from rules.config import GRID
from ui.display import screen
from ui.layout import BOARD_PX, CELL
from ui.theme import (
    BG,
    CYAN,
    GRID_C,
    MUTED,
    ORANGE,
    RED,
    SCAN_SHIP,
    SCAN_WATER,
    SHIP,
    SHIP_HIT,
    SHIP_STEALTH,
    SHIP_SUNK,
    SMALL,
    WATER,
    WHITE,
    YELLOW,
)
from ui.widgets import text


def cell_rect(ox, oy, cell):
    return pygame.Rect(
        ox + cell[1] * CELL,
        oy + cell[0] * CELL,
        CELL,
        CELL
    )


def cell_at(pos, ox, oy):
    """Pixel position -> (row, col), or None if it isn't over the board at (ox, oy)."""
    c, r = (pos[0] - ox) // CELL, (pos[1] - oy) // CELL
    return (r, c) if 0 <= r < GRID and 0 <= c < GRID else None


def highlight(cells, ox, oy, color):
    """Translucent overlay on some cells (hover previews). color is RGBA."""
    tile = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
    tile.fill(color)

    for cell in cells:
        screen.blit(
            tile,
            cell_rect(ox, oy, cell).topleft
        )


def draw_grid(ox, oy):
    # Board background
    pygame.draw.rect(
        screen,
        WATER,
        (ox, oy, BOARD_PX, BOARD_PX),
        border_radius=6
    )

    # Grid lines
    for i in range(GRID + 1):
        x = ox + i * CELL
        y = oy + i * CELL

        pygame.draw.line(
            screen,
            GRID_C,
            (x, oy),
            (x, oy + BOARD_PX),
            1
        )

        pygame.draw.line(
            screen,
            GRID_C,
            (ox, y),
            (ox + BOARD_PX, y),
            1
        )

    # Board border
    pygame.draw.rect(
        screen,
        CYAN,
        (ox, oy, BOARD_PX, BOARD_PX),
        2,
        border_radius=6
    )

    # Column letters
    for i in range(GRID):
        text(
            chr(65 + i),
            (
                ox + i * CELL + CELL // 2,
                oy - 12
            ),
            SMALL,
            MUTED,
            center=True
        )

    # Row numbers
    for i in range(GRID):
        text(
            str(i + 1),
            (
                ox - 14,
                oy + i * CELL + CELL // 2
            ),
            SMALL,
            MUTED,
            center=True
        )


def draw_marker(kind, rect):
    cx, cy = rect.center

    if kind == "hit":
        # Red target
        pygame.draw.circle(
            screen,
            RED,
            (cx, cy),
            11
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (cx, cy),
            11,
            2
        )

        # X
        pygame.draw.line(
            screen,
            WHITE,
            (cx - 6, cy - 6),
            (cx + 6, cy + 6),
            2
        )

        pygame.draw.line(
            screen,
            WHITE,
            (cx + 6, cy - 6),
            (cx - 6, cy + 6),
            2
        )

    elif kind == "miss":
        # Water splash
        pygame.draw.circle(
            screen,
            CYAN,
            (cx, cy),
            7,
            2
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (cx, cy),
            2
        )

    elif kind == "blocked":
        # Shield effect
        pygame.draw.circle(
            screen,
            CYAN,
            (cx, cy),
            11,
            3
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (cx, cy),
            5,
            1
        )

    elif kind == "bomb":
        # Bomb marker
        pygame.draw.circle(
            screen,
            ORANGE,
            (cx, cy),
            11
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (cx, cy),
            11,
            2
        )

        text(
            "B",
            (cx, cy),
            SMALL,
            BG,
            center=True
        )


def draw_own_board(board, ox, oy):
    """Everything is visible: your ships, damage, shields, bomb and the enemy's misses."""
    draw_grid(ox, oy)

    # Ships
    for ship in board.ships:
        for i, cell in enumerate(ship.cells):
            rect = cell_rect(
                ox,
                oy,
                cell
            ).inflate(-5, -5)

            # Ship color
            color = SHIP_STEALTH if ship.stealthed else SHIP

            if i in ship.hit:
                color = SHIP_HIT

            if ship.sunk:
                color = SHIP_SUNK

            # Main ship body
            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=5
            )

            # Ship border
            pygame.draw.rect(
                screen,
                WHITE if not ship.sunk else RED,
                rect,
                1,
                border_radius=5
            )

            # Damage marker
            if i in ship.hit:
                pygame.draw.line(
                    screen,
                    WHITE,
                    rect.topleft,
                    rect.bottomright,
                    2
                )

                pygame.draw.line(
                    screen,
                    WHITE,
                    rect.topright,
                    rect.bottomleft,
                    2
                )

            # Ship identification
            elif i == 0:
                text(
                    ship.name[0],
                    rect.center,
                    SMALL,
                    BG,
                    center=True
                )

            # Shield effect
            if i in ship.shield:
                shield_rect = rect.inflate(2, 2)

                pygame.draw.rect(
                    screen,
                    CYAN,
                    shield_rect,
                    3,
                    border_radius=6
                )

                pygame.draw.circle(
                    screen,
                    CYAN,
                    rect.center,
                    4,
                    1
                )

    # Bomb marker
    if board.bomb:
        r = cell_rect(
            ox,
            oy,
            board.bomb
        )

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (r.centerx, r.top + 5),
                (r.right - 5, r.centery),
                (r.centerx, r.bottom - 5),
                (r.left + 5, r.centery),
            ],
            2
        )

    # Shots
    for cell, kind in board.shots.items():
        if kind != "hit":
            draw_marker(
                kind,
                cell_rect(ox, oy, cell)
            )


def draw_enemy_board(board, ox, oy, reveal=False):
    """Only what you have learned: shots, scans. (reveal=True after the game ends.)"""
    draw_grid(
        ox,
        oy
    )

    # Scanned cells
    for cell, occupied in board.scanned.items():
        rect = cell_rect(
            ox,
            oy,
            cell
        )

        pygame.draw.rect(
            screen,
            SCAN_SHIP if occupied else SCAN_WATER,
            rect.inflate(-2, -2),
            border_radius=3
        )

        if occupied and cell not in board.shots:
            pygame.draw.rect(
                screen,
                YELLOW,
                pygame.Rect(
                    0,
                    0,
                    8,
                    8
                ).move(
                    rect.centerx - 4,
                    rect.centery - 4
                ),
                border_radius=2
            )

    # Reveal enemy ships after game ends
    if reveal:
        for ship in board.ships:
            for i, cell in enumerate(ship.cells):
                rect = cell_rect(
                    ox,
                    oy,
                    cell
                ).inflate(-5, -5)

                color = SHIP_SUNK if ship.sunk else SHIP

                pygame.draw.rect(
                    screen,
                    color,
                    rect,
                    2,
                    border_radius=5
                )

                if i == 0:
                    text(
                        ship.name[0],
                        rect.center,
                        SMALL,
                        color,
                        center=True
                    )

    # Shot markers
    for cell, kind in board.shots.items():
        draw_marker(
            kind,
            cell_rect(ox, oy, cell)
        )