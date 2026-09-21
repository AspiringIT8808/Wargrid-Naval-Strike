"""
OPTIONAL MECHANICS: Bomb, Repair, Shield.

Same shape as abilities.py: repair() and shield() take (game, cell) and return
(error, log_text). To remove a mechanic, delete its function here, its method in
game.py, and its option in ui/app.py.
"""
import random


def detonate_bomb(attacker_board):
    """The trap hurts the attacker's ship with the most HP remaining (ties: random)."""
    alive = [s for s in attacker_board.ships if not s.sunk]
    top = max(s.hp for s in alive)
    ship = random.choice([s for s in alive if s.hp == top])
    seg = random.choice([i for i in range(ship.size) if i not in ship.hit])
    ship.hit.add(seg)                       # the bomb ignores shields
    ship.shield.discard(seg)
    return f"{ship.name} takes 1 damage" + (" and is SUNK!" if ship.sunk else "")


def repair(game, cell):
    if not game.options["repair"]:
        return "Repair is disabled.", None
    board = game.me
    if board.repairs_left <= 0:
        return "No repairs left.", None
    if cell not in board.repairable_cells():
        return "Pick a damaged cell on a ship that is still afloat.", None
    ship = board.ship_at(cell)
    ship.hit.discard(ship.cells.index(cell))
    if board.shots.get(cell) == "hit":
        del board.shots[cell]               # the enemy may shoot this cell again
    board.repairs_left -= 1
    return None, "repairs a ship"


def shield(game, cell):
    if not game.options["shield"]:
        return "Shield is disabled.", None
    board = game.me
    if board.shields_left <= 0:
        return "No shields left.", None
    if cell not in board.shieldable_cells():
        return "Pick an undamaged, unshielded cell of a ship that is afloat.", None
    ship = board.ship_at(cell)
    ship.shield.add(ship.cells.index(cell))
    board.shields_left -= 1
    return None, "raises a shield"
