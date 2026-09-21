"""
SHIP ABILITIES.

Ability         = the uses / cooldown bookkeeping that every ship ability shares.
ABILITY_EFFECTS = what each ability actually DOES. One small function per ability,
                  so each one can be read (or changed) on its own.

An effect function receives (game, ship, target) and returns (error, log_text):
  * error is a string if the action is invalid (nothing must have changed), else None
  * log_text is the sentence for the log, e.g. "uses RECON around C5"
Game.use_ability() takes care of spending the use and ending the turn.
"""
from rules.config import GRID, RECON_SIZE, STEALTH_ROUNDS
from rules.grid import area_cells, cell_name, in_bounds


class Ability:
    def __init__(self, spec):
        self.key = spec["key"]
        self.label = spec["label"]
        self.uses_left = spec["uses"]
        self.cooldown = spec["cooldown"]
        self.cooldown_left = 0

    @property
    def ready(self):
        return self.cooldown_left == 0 and (self.uses_left is None or self.uses_left > 0)

    def spend(self):
        if self.uses_left is not None:
            self.uses_left -= 1
        self.cooldown_left = self.cooldown

    def tick(self):                       # called at the start of the owner's turn
        self.cooldown_left = max(0, self.cooldown_left - 1)


# ----- the effects -----------------------------------------------------------
def barrage_attacks(game, ship, target):
    """Frigate. The ability REPLACES the normal attack: two shots instead of one."""
    game.attacks_left = 4
    return None, "uses BARRAGE ATTACK (two shots this turn)"


def relocate(game, ship, target):
    """Destroyer. target = list of the new cells."""
    error = game.me.check_move(ship, target) if target else "Pick a new position."
    if error:
        return error, None
    ship.cells = list(target)             # damage & shields travel with the ship
    return None, "uses RELOCATE (a ship moved)"


def recon(game, ship, target):
    """Carrier. target = (row, col) centre of the reveal."""
    if target is None or not in_bounds(target):
        return "Pick a cell on the enemy board.", None
    game.foe.scan(area_cells(target, RECON_SIZE))
    return None, f"uses RECON around {cell_name(target)}"


def row_scan(game, ship, target):
    """Cruiser. target = row index."""
    if not isinstance(target, int) or not 0 <= target < GRID:
        return "Pick a row.", None
    game.foe.scan([(target, c) for c in range(GRID)])
    return None, f"uses ROW SCAN on row {target + 1}"


def stealth(game, ship, target):
    """Submarine. The one exception to 'ability OR attack': it also gets one shot."""
    ship.stealth_left = STEALTH_ROUNDS
    game.attacks_left = 1
    return None, "uses STEALTH (Submarine untargetable) and gets one shot"


# ability key (from config.SHIP_SPECS) -> effect function
ABILITY_EFFECTS = {
    "barrage_attacks": barrage_attacks,
    "relocate": relocate,
    "recon": recon,
    "row_scan": row_scan,
    "stealth": stealth,
}
