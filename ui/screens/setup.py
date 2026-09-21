"""Fleet deployment: place each ship (and the bomb) on your own board."""
import pygame

from rules.board import Board
from rules.config import SHIP_SPECS, SPEC_BY_NAME
from rules.grid import in_bounds, line_cells
from ui.board_view import cell_at, draw_own_board, highlight
from ui.display import W, screen
from ui.layout import BOARD_Y, SETUP_X
from ui.screens.base import Screen
from ui.theme import ACCENT, BIG, MUTED, PANEL_2, SMALL, TEXT
from ui.widgets import Button, text


class SetupScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.index = 0                      # which player is deploying (0 or 1)
        self.board = Board()
        self.sel = None                     # selected item: a ship name, "Bomb", or None
        self.horizontal = True
        self.btn_random = Button((640, 0, 190, 44), "RANDOMIZE ALL")
        self.btn_ready = Button((850, 0, 190, 44), "READY")

    # ----- flow -----
    def begin(self):
        """Start (or restart) deployment for player `self.index`."""
        self.board = Board()
        self.sel = SHIP_SPECS[0]["name"]
        self.horizontal = True
        self.app.goto("setup")

    def finish(self):
        app = self.app
        app.game.boards[self.index] = self.board
        if app.mode == "ai":
            app.game.boards[1].random_setup(app.options["bomb"])
            app.screens["play"].start_battle()
        elif self.index == 0:
            self.index = 1
            app.handoff(["Player 2: deploy your fleet", "Player 1, look away!"], self.begin)
        else:
            app.handoff(["Both fleets are ready.", "Player 1 starts - pass the device."],
                        app.screens["play"].start_battle)

    # ----- item list -----
    def items(self):
        return [s["name"] for s in SHIP_SPECS] + (["Bomb"] if self.app.options["bomb"] else [])

    def is_placed(self, item):
        b = self.board
        return b.bomb is not None if item == "Bomb" else b.get_ship(item) is not None

    def next_unplaced(self):
        return next((i for i in self.items() if not self.is_placed(i)), None)

    def pick_up(self, item):
        if item == "Bomb":
            self.board.bomb = None
        else:
            self.board.remove_ship(item)
        self.sel = item

    def item_rect(self, i):
        return pygame.Rect(640, 190 + i * 44, 400, 38)

    def ready(self):
        return self.board.setup_done(self.app.options["bomb"])

    def layout_buttons(self):
        y = 190 + len(self.items()) * 44 + 20
        self.btn_random.rect.y = self.btn_ready.rect.y = y

    # ----- input -----
    def on_event(self, e):
        b = self.board
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                self.horizontal = not self.horizontal
            elif e.key == pygame.K_RETURN and self.ready():
                self.finish()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 3:
                self.horizontal = not self.horizontal
            elif e.button == 1:
                self.layout_buttons()
                for i, item in enumerate(self.items()):
                    if self.item_rect(i).collidepoint(e.pos):
                        self.pick_up(item)
                        return
                if self.btn_random.hit(e.pos):
                    b.random_setup(self.app.options["bomb"])
                    self.sel = None
                elif self.btn_ready.hit(e.pos) and self.ready():
                    self.finish()
                cell = cell_at(e.pos, SETUP_X, BOARD_Y)
                if cell is None:
                    return
                if self.sel == "Bomb":
                    if b.set_bomb(cell):
                        self.sel = self.next_unplaced()
                elif self.sel:
                    spec = SPEC_BY_NAME[self.sel]
                    if b.place_ship(spec, line_cells(cell, spec["size"], self.horizontal)):
                        self.sel = self.next_unplaced()
                else:                           # nothing selected: click a ship/bomb to pick it up
                    ship = b.ship_at(cell)
                    if ship:
                        self.pick_up(ship.name)
                    elif cell == b.bomb:
                        self.pick_up("Bomb")

    # ----- drawing -----
    def draw(self):
        b = self.board
        text(f"FLEET DEPLOYMENT - {self.game.names[self.index].upper()}", (W // 2, 40), BIG, ACCENT, center=True)
        draw_own_board(b, SETUP_X, BOARD_Y)

        hover = cell_at(pygame.mouse.get_pos(), SETUP_X, BOARD_Y)
        if hover and self.sel == "Bomb":
            highlight([hover], SETUP_X, BOARD_Y, (239, 166, 70, 110) if b.ship_at(hover) is None else (230, 78, 92, 110))
        elif hover and self.sel:
            cells = line_cells(hover, SPEC_BY_NAME[self.sel]["size"], self.horizontal)
            color = (73, 207, 180, 110) if b.can_place(cells) else (230, 78, 92, 110)
            highlight([c for c in cells if in_bounds(c)], SETUP_X, BOARD_Y, color)

        text("Pick an item, then click the board.  R / right-click rotates.", (640, 105), SMALL, MUTED)
        text("Click a placed ship to pick it up and move it.", (640, 127), SMALL, MUTED)
        if self.app.options["bomb"]:
            text("Bomb: hidden trap on open water. If the enemy fires there,", (640, 149), SMALL, MUTED)
            text("THEIR healthiest ship takes 1 damage.", (640, 165), SMALL, MUTED)
        for i, item in enumerate(self.items()):
            rect = self.item_rect(i)
            size = f" ({SPEC_BY_NAME[item]['size']})" if item != "Bomb" else ""
            state = "placed" if self.is_placed(item) else "-"
            pygame.draw.rect(screen, PANEL_2, rect, border_radius=6)
            pygame.draw.rect(screen, ACCENT if self.sel == item else (75, 95, 110), rect, 2, border_radius=6)
            text(f"{item}{size}", (rect.x + 14, rect.y + 10), SMALL, TEXT)
            text(state, (rect.right - 70, rect.y + 10), SMALL, ACCENT if state == "placed" else MUTED)
        self.layout_buttons()
        self.btn_random.draw()
        self.btn_ready.draw(enabled=self.ready())
