"""One player's board: ship placement, incoming shots, scans, bomb."""
import random

from rules.config import GRID, REPAIR_USES, SHIELD_USES, SHIP_SPECS
from rules.grid import in_bounds, line_cells
from rules.ship import Ship


class Board:
    """
    shots   = every shot fired AT this board, cell -> "hit" | "miss" | "blocked" | "bomb".
              This doubles as the attacker's map of what they know.
    scanned = cells revealed to the enemy by Recon / Row Scan, cell -> True if a ship
              was there at the moment of the scan.
    """

    def __init__(self):
        self.ships = []
        self.shots = {}
        self.scanned = {}
        self.bomb = None                  # hidden trap cell (on water) or None
        self.repairs_left = REPAIR_USES
        self.shields_left = SHIELD_USES

    # ----- lookups -----
    def get_ship(self, name):
        return next((s for s in self.ships if s.name == name), None)

    def ship_at(self, cell):
        return next((s for s in self.ships if cell in s.cells), None)

    def fleet_sunk(self):
        return bool(self.ships) and all(s.sunk for s in self.ships)

    def can_fire(self, cell):
        # A cell whose shield just blocked a shot can be fired at again.
        return in_bounds(cell) and self.shots.get(cell) in (None, "blocked")

    # ----- setup -----
    def can_place(self, cells, ignore=None):
        for cell in cells:
            if not in_bounds(cell) or cell == self.bomb:
                return False
            ship = self.ship_at(cell)
            if ship is not None and ship is not ignore:
                return False
        return True

    def place_ship(self, spec, cells):
        if len(cells) != spec["size"] or not self.can_place(cells):
            return False
        self.ships.append(Ship(spec, cells))
        return True

    def remove_ship(self, name):
        self.ships = [s for s in self.ships if s.name != name]

    def set_bomb(self, cell):
        if in_bounds(cell) and self.ship_at(cell) is None:
            self.bomb = cell
            return True
        return False

    def setup_done(self, with_bomb):
        return len(self.ships) == len(SHIP_SPECS) and (not with_bomb or self.bomb is not None)

    def random_setup(self, with_bomb):
        self.ships, self.bomb = [], None
        for spec in SHIP_SPECS:
            while True:
                anchor = (random.randrange(GRID), random.randrange(GRID))
                cells = line_cells(anchor, spec["size"], random.random() < 0.5)
                if self.can_place(cells):
                    break
            self.place_ship(spec, cells)
        if with_bomb:
            while not self.set_bomb((random.randrange(GRID), random.randrange(GRID))):
                pass

    # ----- movement (Destroyer) -----
    def check_move(self, ship, cells):
        """Return an error string, or None if `ship` may move onto `cells`."""
        if len(cells) != ship.size or not self.can_place(cells, ignore=ship):
            return "That position is off the board or overlaps something."
        if set(cells) == set(ship.cells):
            return "Pick a different position."
        if not all(self.can_fire(c) for c in cells):
            return "Can't move onto cells the enemy has already fired at."
        return None

    # ----- damage -----
    def receive_attack(self, cell):
        """Resolve one shot. Returns (result, ship_or_None)."""
        if cell == self.bomb:
            self.shots[cell] = "bomb"
            self.bomb = None
            return "bomb", None

        ship = self.ship_at(cell)

        if ship is None:
            self.shots[cell] = "miss"
            return "miss", None

        if ship.stealthed:
            return "stealth", ship

        i = ship.cells.index(cell)

        if i in ship.shield:
            ship.shield.discard(i)
            self.shots[cell] = "blocked"
            return "blocked", ship

        ship.hit.add(i)
        self.shots[cell] = "hit"
        return "hit", ship

    def scan(self, cells):
        for cell in cells:
            self.scanned[cell] = self.ship_at(cell) is not None

    # ----- helpers for Repair / Shield -----
    def repairable_cells(self):
        return [s.cells[i] for s in self.ships if not s.sunk for i in s.hit]

    def shieldable_cells(self):
        return [s.cells[i] for s in self.ships if not s.sunk
                for i in range(s.size) if i not in s.hit and i not in s.shield]
