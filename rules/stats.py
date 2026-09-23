"""
BATTLE STATISTICS.

Tracks what happened during a match so the post-game "After-Action Report"
(ui/screens/stats.py) has something to show. This module only RECORDS events
that rules/game.py has already resolved - it never decides anything itself,
same spirit as extras.py and abilities.py.

Game.stats is created in Game.begin() and fed by a handful of one-line hooks
inside Game.attack / use_ability / use_repair / use_shield / end_turn.
"""
import time


class PlayerStats:
    def __init__(self, name):
        self.name = name
        self.shots = 0
        self.hits = 0
        self.misses = 0
        self.blocked = 0
        self.bombs_triggered = 0
        self.ships_sunk = 0          # enemy ships this player sank
        self.abilities_used = {}     # ability label -> count
        self.repairs_used = 0
        self.shields_used = 0
        self.damage_taken = 0        # segments this player's own fleet lost

    @property
    def accuracy(self):
        return (self.hits / self.shots * 100) if self.shots else 0.0

    def record_ability(self, label):
        self.abilities_used[label] = self.abilities_used.get(label, 0) + 1


class BattleStats:
    def __init__(self, names):
        self.players = [PlayerStats(names[0]), PlayerStats(names[1])]
        self.turns = 0
        self.started_at = time.time()
        self.ended_at = None

    def record_shot(self, attacker_idx, result, ship_sunk):
        p = self.players[attacker_idx]
        p.shots += 1
        if result == "hit":
            p.hits += 1
            self.players[1 - attacker_idx].damage_taken += 1
            if ship_sunk:
                p.ships_sunk += 1
        elif result == "miss":
            p.misses += 1
        elif result == "blocked":
            p.blocked += 1
        elif result == "bomb":
            p.bombs_triggered += 1
            p.damage_taken += 1          # the bomb hurts the attacker's own fleet

    def record_ability(self, player_idx, label):
        self.players[player_idx].record_ability(label)

    def record_repair(self, player_idx):
        self.players[player_idx].repairs_used += 1

    def record_shield(self, player_idx):
        self.players[player_idx].shields_used += 1

    def record_turn(self):
        self.turns += 1

    def finish(self):
        self.ended_at = time.time()

    @property
    def duration_seconds(self):
        end = self.ended_at or time.time()
        return end - self.started_at
