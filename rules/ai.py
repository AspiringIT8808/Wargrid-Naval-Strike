"""Very simple computer opponent. Uses only the public Game actions."""
import random

from rules.config import GRID


def ai_pick_cell(game):
    """Hunt/target: finish what it has hit, otherwise fire on a checkerboard."""
    board = game.foe                            # board.shots is the AI's knowledge
    targets = []
    for (r, c), kind in board.shots.items():
        if kind == "blocked":                   # a shield saved it -> shoot again
            return (r, c)
        if kind == "hit":
            ship = board.ship_at((r, c))
            if ship is not None and ship.sunk:  # sinking is public info, skip finished ships
                continue
            targets += [n for n in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)) if board.can_fire(n)]
    if targets:
        return random.choice(targets)
    free = [(r, c) for r in range(GRID) for c in range(GRID) if board.can_fire((r, c))]
    return random.choice([x for x in free if (x[0] + x[1]) % 2 == 0] or free)


def ai_step(game):
    """One AI action. Call repeatedly until the turn passes to the other player."""
    if game.attacks_left == 0:
        for name, chance in (("Frigate", 0.25), ("Submarine", 0.15)):
            ship = game.me.get_ship(name)
            if ship and not ship.sunk and ship.ability.ready and random.random() < chance:
                return game.use_ability(name)
    return game.attack(ai_pick_cell(game))
