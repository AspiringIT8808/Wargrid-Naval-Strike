"""
THE BATTLE SCREEN.

Left = your fleet, right = enemy waters, middle = fleet status, bottom = action buttons.
Clicking never changes the game directly: it calls Game.attack / use_ability / use_repair /
use_shield (see self.click_board and self.click_action) and shows whatever comes back.
"""
import time
import pygame
from rules.game import Game
from rules.ai import ai_step
from rules.config import GRID, RECON_SIZE, SHIP_BY_KEY, SHIP_SPECS
from rules.grid import area_cells, in_bounds, line_cells
from ui.board_view import cell_at, draw_enemy_board, draw_own_board, highlight
from ui.display import W
from ui.layout import BOARD_Y, LEFT_X, RIGHT_X
from ui.panels import draw_fleet_status
from ui.screens.base import Screen
from ui.theme import ACCENT, BIG, FONT, MUTED, ORANGE, SMALL, TEXT
from ui.widgets import Button, text

ACTIONS = ([dict(id=s["key"], ship=s["name"], label=s["label"]) for s in SHIP_SPECS] +
           [dict(id="repair", ship=None, label="REPAIR"),
            dict(id="shield", ship=None, label="SHIELD")])


class PlayScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.view = 0
        self.pass_pending = False
        self.selected = None
        self.horizontal = True
        self.msg = ""
        self.ai_next = 0
        self.action_btns = [Button((50 + i * 165, 655, 155, 62)) for i in range(len(ACTIONS))]
        self.pass_btn = Button((340, 655, 600, 62))
        self.settings_btn = Button((20, 15, 35, 35))

    def start_battle(self):
        self.game.begin()
        self.view = 0
        self.pass_pending = False
        self.selected = None
        self.horizontal = True
        self.msg = "Battle begins!"
        self.app.goto("play")

    def resume_after_pass(self):
        self.view = self.game.current
        self.pass_pending = False
        self.selected = None
        self.msg = "Your move."
        self.app.goto("play")

    def restart_level(self):
        self.app.game = Game(self.app.options)
        self.app.game.names = [
            "Player 1",
            "Computer" if self.app.mode == "ai" else "Player 2"
        ]

        self.view = 0
        self.pass_pending = False
        self.selected = None
        self.horizontal = True
        self.msg = ""
        self.ai_next = 0

        setup = self.app.screens["setup"]
        setup.index = 0
        setup.begin()

    def can_act(self):
        g = self.game
        return g.winner is None and g.current == self.view and not self.pass_pending

    def action_state(self, a):
        mine = self.game.boards[self.view]
        if a["ship"]:
            ship = mine.get_ship(a["ship"])
            if ship is None or ship.sunk:
                return False, "SUNK"
            ab = ship.ability
            if ab.uses_left == 0:
                return False, "used up"
            if ab.cooldown_left:
                return False, f"cooldown {ab.cooldown_left}"
            return True, f"{ship.name} x{'inf' if ab.uses_left is None else ab.uses_left}"
        if not self.app.options[a["id"]]:
            return False, "off"
        if a["id"] == "repair":
            return mine.repairs_left > 0 and bool(mine.repairable_cells()), f"{mine.repairs_left} left"
        return mine.shields_left > 0 and bool(mine.shieldable_cells()), f"{mine.shields_left} left"

    def prompt(self):
        g, v = self.game, self.view
        name = g.names[v].upper()
        if g.winner is not None:
            return "GAME OVER"
        if self.pass_pending:
            return f"{name}: turn over."
        if g.current != v:
            return f"{g.names[g.current].upper()} IS THINKING..."
        if g.attacks_left > 0:
            return f"{name}: {g.attacks_left} shot(s) left - click enemy waters"
        hints = {
            None: "ATTACK (click enemy waters) OR use ONE ability",
            "recon": f"RECON: click a cell to scan {RECON_SIZE}x{RECON_SIZE} around it",
            "row_scan": "ROW SCAN: click any cell in the row you want revealed",
            "relocate": "RELOCATE: click where the Destroyer's top-left goes (R rotates)",
            "repair": "REPAIR: click a damaged cell on YOUR board",
            "shield": "SHIELD: click one of YOUR ship cells to protect"
        }
        return f"{name}: {hints[self.selected]}"

    def on_event(self, e):
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:
                if self.selected is not None:
                    self.selected = None
                else:
                    self.app.open_settings("play")
                return

            if e.key == pygame.K_r:
                self.horizontal = not self.horizontal

            elif e.key in (pygame.K_SPACE, pygame.K_RETURN) and self.pass_pending:
                self.pass_device()

        elif e.type == pygame.MOUSEBUTTONDOWN:

            # Right-click cancels the currently selected ability.
            if e.button == 3:
                self.selected = None

            # Left-click
            elif e.button == 1:

                # Open the dedicated ESC Settings screen.
                if self.settings_btn.hit(e.pos):
                    self.app.open_settings("play")
                    self.selected = None
                    return

                if self.pass_pending:
                    if self.pass_btn.hit(e.pos):
                        self.pass_device()

                elif self.can_act():
                    for a, btn in zip(ACTIONS, self.action_btns):
                        if btn.hit(e.pos):
                            self.click_action(a)
                            return

                    self.click_board(e.pos)

    def click_action(self, a):
        enabled, _ = self.action_state(a)
        if not enabled or self.game.attacks_left > 0:
            self.msg = "That action isn't available right now."
        elif a["id"] in ("barrage_attacks", "stealth"):
            self.do(lambda: self.game.use_ability(a["ship"]))
        else:
            self.selected = None if self.selected == a["id"] else a["id"]
            self.msg = ""

    def click_board(self, pos):
        g, sel = self.game, self.selected
        enemy = cell_at(pos, RIGHT_X, BOARD_Y)
        own = cell_at(pos, LEFT_X, BOARD_Y)

        if sel is None:
            if enemy:
                self.do(lambda: g.attack(enemy))
        elif sel in ("recon", "row_scan"):
            if enemy:
                self.do(lambda: g.use_ability(
                    SHIP_BY_KEY[sel],
                    enemy if sel == "recon" else enemy[0]
                ))
        elif sel == "relocate":
            if own:
                ship = g.boards[self.view].get_ship(SHIP_BY_KEY[sel])
                cells = line_cells(own, ship.size, self.horizontal)
                self.do(lambda: g.use_ability(ship.name, cells))
        elif own:
            self.do(lambda: g.use_repair(own) if sel == "repair" else g.use_shield(own))

    def do(self, action):
        who = self.game.current
        ok, self.msg = action()
        if ok:
            self.selected = None
        self.after_action(who)

    def after_action(self, who):
        g = self.game
        if g.winner is not None:
            self.app.goto("gameover")
        elif g.current != who:
            if self.app.mode == "duo":
                self.pass_pending = True
            elif g.current == 1:
                self.ai_next = time.time() + 0.8
            else:
                self.msg += "   -  Your turn!"

    def pass_device(self):
        g = self.game
        lines = [
            f"{g.names[g.current]}'s turn",
            ""
        ] + g.last_turn_log[-3:] + [
            "",
            "Pass the device, then click to continue."
        ]
        self.app.handoff(lines, self.resume_after_pass)

    def update(self):
        g = self.game
        if self.app.mode == "ai" and g.current == 1 and g.winner is None and time.time() >= self.ai_next:
            who = g.current
            _, self.msg = ai_step(g)
            self.ai_next = time.time() + 0.7
            self.after_action(who)

    def draw(self):
        g, v = self.game, self.view
        mine, theirs = g.boards[v], g.boards[1 - v]
        over = g.winner is not None

        text(
            "WARGRID: NAVAL STRIKE // TACTICAL EDITION",
            (W // 2, 26),
            BIG,
            ACCENT,
            center=True
        )

        own_label = "YOUR FLEET" if self.app.mode == "ai" else f"{g.names[v].upper()} - FLEET"

        text(own_label, (LEFT_X, 60), FONT, TEXT)
        text("ENEMY WATERS", (RIGHT_X, 60), FONT)

        draw_own_board(mine, LEFT_X, BOARD_Y)
        draw_enemy_board(theirs, RIGHT_X, BOARD_Y, reveal=over)

        if self.can_act():
            self.draw_previews(mine, theirs)

        draw_fleet_status(mine, theirs)

        text(
            self.prompt(),
            (50, 598),
            FONT,
            ACCENT if self.can_act() else ORANGE
        )

        text(self.msg, (50, 624), SMALL, TEXT)

        if self.pass_pending:
            self.pass_btn.draw(
                label=f"END TURN  -  pass to {g.names[g.current]}  (SPACE)"
            )
        else:
            can_start = self.can_act() and g.attacks_left == 0
            for a, btn in zip(ACTIONS, self.action_btns):
                enabled, sub = self.action_state(a)
                btn.draw(
                    enabled and can_start,
                    self.selected == a["id"],
                    sub,
                    a["label"]
                )

        self.settings_btn.draw(
            True,
            False,
            None,
            "*"
        )

        text(
            "ESC / right-click cancels a selection.   Ability turns end your turn; except for Submarine and Frigate.",
            (50, 735),
            SMALL,
            MUTED
        )

    def draw_previews(self, mine, theirs):
        enemy = cell_at(pygame.mouse.get_pos(), RIGHT_X, BOARD_Y)
        own = cell_at(pygame.mouse.get_pos(), LEFT_X, BOARD_Y)
        sel = self.selected
        good = (73, 207, 180, 100)

        if enemy and sel is None and theirs.can_fire(enemy):
            highlight([enemy], RIGHT_X, BOARD_Y, good)

        elif enemy and sel == "recon":
            highlight(
                area_cells(enemy, RECON_SIZE),
                RIGHT_X,
                BOARD_Y,
                (244, 218, 102, 90)
            )

        elif enemy and sel == "row_scan":
            highlight(
                [(enemy[0], c) for c in range(GRID)],
                RIGHT_X,
                BOARD_Y,
                (244, 218, 102, 90)
            )

        elif sel == "relocate" and own:
            ship = mine.get_ship(SHIP_BY_KEY[sel])
            cells = line_cells(own, ship.size, self.horizontal)
            color = (
                good
                if mine.check_move(ship, cells) is None
                else (230, 78, 92, 110)
            )
            highlight(
                [c for c in cells if in_bounds(c)],
                LEFT_X,
                BOARD_Y,
                color
            )

        elif sel == "repair":
            highlight(
                mine.repairable_cells(),
                LEFT_X,
                BOARD_Y,
                (244, 218, 102, 90)
            )

        elif sel == "shield":
            highlight(
                mine.shieldable_cells(),
                LEFT_X,
                BOARD_Y,
                (90, 200, 240, 70)
            )