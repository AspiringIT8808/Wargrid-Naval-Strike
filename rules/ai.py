"""Picks which computer opponent to run based on game.difficulty.

Keeps `from rules.ai import ai_step` working everywhere it's already used -
only this file changed, nothing that calls ai_step needs to know about the
three difficulty modules.
"""
from rules import ai_beginner, ai_intermediate, ai_expert

AI_LEVELS = {
    "beginner": ai_beginner,
    "intermediate": ai_intermediate,
    "expert": ai_expert,
}


def ai_step(game):
    module = AI_LEVELS.get(getattr(game, "difficulty", "intermediate"), ai_intermediate)
    return module.ai_step(game)