"""Expert computer opponent.

Targeting:
  1. A shield just blocked a shot -> finish that cell off, it's unshielded now.
  2. Recon / Row Scan already showed us a ship is sitting somewhere -> free hit.
  3. Two or more unsunk hits on the same ship -> lock onto that line and fire
     off the confirmed end(s), instead of poking randomly at all four sides.
  4. Otherwise: a probability-density map. For every still-possible cell, count
     how many ways each remaining ship (by size) could be placed through it -
     the classic "where is a ship most likely to be" heuristic - and fire on
     the busiest cell. This naturally favours the centre and open parity gaps
     without hardcoding a checkerboard.

Abilities (every ship, used with a reason, not a coin flip):
  - Frigate  BARRAGE: fired only while actively chasing a hit - an extra shot
    is worth the most right when it can capitalize on one.
  - Destroyer RELOCATE: used defensively, to pull a damaged Destroyer off a
    cell the enemy already knows about, onto an unshot patch of its own board.
  - Carrier RECON / Cruiser ROW SCAN: used only when there's no active hunt,
    i.e. it's about to guess blind anyway - better to spend the turn buying
    information than to fire into the dark. Recon centres and the scanned row
    are chosen using the same density map, so the scout goes where a ship is
    statistically most likely to be.
  - Submarine STEALTH: saved for when its own fleet is genuinely hurting (2+
    damaged ships), since it both hides a ship for a round and still shoots.
  - Repair / Shield: used between hunts to patch its biggest damaged ship or
    pre-emptively shield its biggest healthy one, never in the middle of
    chasing a kill.

`remaining_sizes()` only trusts information the AI is entitled to: it treats
a ship's size/identity as known only once one of its cells has been hit (the
game already reveals ship identity via `board.ship_at`, and sinking is public
info), matching the "public actions only" spirit of the simpler AIs.
"""
import random

from rules.config import GRID, RECON_SIZE, SHIP_SPECS
from rules.grid import area_cells, in_bounds, line_cells


# ----- reading the board -----------------------------------------------------
def remaining_sizes(board):
    """Sizes of enemy ships not yet confirmed sunk."""
    sunk = set()
    for cell, kind in board.shots.items():
        if kind == "hit":
            ship = board.ship_at(cell)
            if ship is not None and ship.sunk:
                sunk.add(ship.name)
    return [s["size"] for s in SHIP_SPECS if s["name"] not in sunk]


def possible(board, cell):
    """Could a ship still occupy this cell, as far as we're allowed to know?"""
    return board.shots.get(cell) not in ("miss", "bomb")


def density_map(board):
    """For every still-fireable cell: how many remaining-ship placements cover it."""
    scores = {}
    for size in remaining_sizes(board):
        for r in range(GRID):
            for c in range(GRID):
                for dr, dc in ((0, 1), (1, 0)):
                    line = [(r + dr * i, c + dc * i) for i in range(size)]
                    if all(in_bounds(cell) and possible(board, cell) for cell in line):
                        for cell in line:
                            if board.can_fire(cell):
                                scores[cell] = scores.get(cell, 0) + 1
    return scores


def hunt_targets(board):
    """Cells worth shooting: a freshly-unshielded cell, or a hit line to chase."""
    for (r, c), kind in board.shots.items():
        if kind == "blocked":
            return [(r, c)]

    by_ship = {}
    for cell, kind in board.shots.items():
        if kind != "hit":
            continue
        ship = board.ship_at(cell)
        if ship is None or ship.sunk:
            continue
        by_ship.setdefault(id(ship), []).append(cell)

    targets = []
    for hits in by_ship.values():
        rows = {r for r, _ in hits}
        cols = {c for _, c in hits}
        if len(hits) >= 2 and len(rows) == 1:
            r = hits[0][0]
            cs = sorted(c for _, c in hits)
            targets += [t for t in ((r, cs[0] - 1), (r, cs[-1] + 1)) if board.can_fire(t)]
        elif len(hits) >= 2 and len(cols) == 1:
            c = hits[0][1]
            rs = sorted(r for r, _ in hits)
            targets += [t for t in ((rs[0] - 1, c), (rs[-1] + 1, c)) if board.can_fire(t)]
        else:
            for (r, c) in hits:
                targets += [n for n in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if board.can_fire(n)]
    return targets


def ai_pick_cell(board):
    targets = hunt_targets(board)
    if targets and board.shots.get(targets[0]) == "blocked":
        return targets[0]

    scanned_hits = [c for c, present in board.scanned.items() if present and board.can_fire(c)]
    if scanned_hits:
        return random.choice(scanned_hits)

    if targets:
        return random.choice(targets)

    scores = density_map(board)
    if scores:
        best = max(scores.values())
        return random.choice([c for c, v in scores.items() if v == best])

    free = [(r, c) for r in range(GRID) for c in range(GRID) if board.can_fire((r, c))]
    return random.choice(free)


# ----- scouting targets for Carrier / Cruiser --------------------------------
def best_recon_center(board):
    scores = density_map(board)
    best_cell, best_score = None, -1
    for r in range(GRID):
        for c in range(GRID):
            if (r, c) in board.scanned:
                continue
            total = sum(scores.get(cell, 0) for cell in area_cells((r, c), RECON_SIZE))
            if total > best_score:
                best_cell, best_score = (r, c), total
    return best_cell


def best_row(board):
    scores = density_map(board)
    best_row_idx, best_score = None, -1
    for r in range(GRID):
        unknown = [c for c in range(GRID) if (r, c) not in board.scanned and board.can_fire((r, c))]
        if not unknown:
            continue
        total = sum(scores.get((r, c), 0) for c in unknown)
        if total > best_score:
            best_row_idx, best_score = r, total
    return best_row_idx


# ----- self-preservation: Destroyer / Repair / Shield ------------------------
def find_relocation(board, ship):
    """A same-size spot for `ship`, on its own board, the enemy hasn't shot at yet."""
    candidates = []
    for r in range(GRID):
        for c in range(GRID):
            for horizontal in (True, False):
                cells = line_cells((r, c), ship.size, horizontal)
                if board.check_move(ship, cells) is None:
                    candidates.append(cells)
    return random.choice(candidates) if candidates else None


def best_repair_cell(board):
    cells = board.repairable_cells()
    return max(cells, key=lambda cell: board.ship_at(cell).size) if cells else None


def best_shield_cell(board):
    cells = board.shieldable_cells()
    return max(cells, key=lambda cell: board.ship_at(cell).size) if cells else None


# ----- turn logic --------------------------------------------------------------
def ai_step(game):
    """One AI action. Call repeatedly until the turn passes to the other player."""
    board = game.foe
    me = game.me

    if game.attacks_left == 0:
        hunting = bool(hunt_targets(board))

        # Press the advantage: an extra shot is worth the most while chasing a hit.
        frigate = me.get_ship("Frigate")
        if hunting and frigate and not frigate.sunk and frigate.ability.ready:
            return game.use_ability("Frigate")

        # Pull a damaged Destroyer out of danger before it gets finished off.
        destroyer = me.get_ship("Destroyer")
        if destroyer and not destroyer.sunk and destroyer.hit and destroyer.ability.ready:
            spot = find_relocation(me, destroyer)
            if spot:
                return game.use_ability("Destroyer", spot)

        if not hunting:
            # Patch up whichever damaged ship is worth the most hull.
            if game.options["repair"] and me.repairs_left > 0:
                cell = best_repair_cell(me)
                if cell and random.random() < 0.5:
                    return game.use_repair(cell)

            # Pre-emptively shield the fleet's biggest healthy asset.
            if game.options["shield"] and me.shields_left > 0:
                cell = best_shield_cell(me)
                if cell and random.random() < 0.3:
                    return game.use_shield(cell)

            # No live lead: buy information instead of guessing blind.
            carrier = me.get_ship("Carrier")
            if carrier and not carrier.sunk and carrier.ability.ready and random.random() < 0.5:
                center = best_recon_center(board)
                if center:
                    return game.use_ability("Carrier", center)

            cruiser = me.get_ship("Cruiser")
            if cruiser and not cruiser.sunk and cruiser.ability.ready and random.random() < 0.4:
                row = best_row(board)
                if row is not None:
                    return game.use_ability("Cruiser", row)

        # Heavily damaged: vanish for a round and still get a shot in.
        sub = me.get_ship("Submarine")
        if sub and not sub.sunk and sub.ability.ready:
            damaged = sum(1 for s in me.ships if not s.sunk and s.hit)
            if damaged >= 2 and random.random() < 0.5:
                return game.use_ability("Submarine")

    return game.attack(ai_pick_cell(board))