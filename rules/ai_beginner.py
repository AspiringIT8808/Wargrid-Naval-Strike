"""Beginner computer opponent.

Fires at a random legal cell every time. It never follows up on a hit (no
hunt/target), never reads scan reveals, and never uses ship abilities.
Meant to be an easy, occasionally lucky, mostly-losing opponent.
"""
import random

from rules.config import GRID


def ai_pick_cell(game):
    board = game.foe
    free = [(r, c) for r in range(GRID) for c in range(GRID) if board.can_fire((r, c))]
    return random.choice(free)


def ai_step(game):
    """One AI action. Call repeatedly until the turn passes to the other player."""
    return game.attack(ai_pick_cell(game))