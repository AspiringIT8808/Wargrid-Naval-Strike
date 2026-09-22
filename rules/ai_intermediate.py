"""Intermediate computer opponent.

Same hunt/target + checkerboard search as a basic AI, but ability timing is
tuned instead of being a flat coin flip: it saves the Frigate's extra shots
for when it already has a hit to chase, and reaches for the Submarine's
stealth when its own fleet is taking damage. It still ignores Destroyer,
Carrier and Cruiser - those need real target selection (see the Expert AI).
"""
import random

from rules.config import GRID


def hunt_targets(board):
    """Cells worth shooting because of a shield-block or an unsunk hit."""
    for (r, c), kind in board.shots.items():
        if kind == "blocked":
            return [(r, c)]  # a shield just came down here - always finish it first

    targets = []
    for (r, c), kind in board.shots.items():
        if kind != "hit":
            continue
        ship = board.ship_at((r, c))
        if ship is not None and ship.sunk:      # sinking is public info, nothing left to chase
            continue
        targets += [n for n in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if board.can_fire(n)]
    return targets


def ai_pick_cell(board):
    targets = hunt_targets(board)
    if targets:
        return random.choice(targets)
    free = [(r, c) for r in range(GRID) for c in range(GRID) if board.can_fire((r, c))]
    return random.choice([x for x in free if (x[0] + x[1]) % 2 == 0] or free)


def ai_step(game):
    """One AI action. Call repeatedly until the turn passes to the other player."""
    board = game.foe
    if game.attacks_left == 0:
        hunting = bool(hunt_targets(board))

        frigate = game.me.get_ship("Frigate")
        if frigate and not frigate.sunk and frigate.ability.ready:
            # An extra shot is worth far more while it already has a target to chase.
            chance = 0.65 if hunting else 0.2
            if random.random() < chance:
                return game.use_ability("Frigate")

        sub = game.me.get_ship("Submarine")
        if sub and not sub.sunk and sub.ability.ready:
            damaged = sum(1 for s in game.me.ships if not s.sunk and s.hit)
            chance = 0.45 if damaged >= 2 else 0.15
            if random.random() < chance:
                return game.use_ability("Submarine")

    return game.attack(ai_pick_cell(board))