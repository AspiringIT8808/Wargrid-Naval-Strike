"""
THE GAME: whose turn it is, and the actions a player can take.

The UI only ever calls these methods:  attack / use_ability / use_repair / use_shield.
Each returns (ok, text). If ok is False nothing changed and text is the reason;
if ok is True, text is the log line for what happened.

Where things live:
  what each ship ability does ..... rules/abilities.py
  bomb / repair / shield .......... rules/extras.py
  hit / miss / stealth / shield
  resolution on a single cell ..... rules/board.py  (Board.receive_attack)
  after-battle statistics .......... rules/stats.py  (Game.stats)
"""
from rules import extras
from rules.abilities import ABILITY_EFFECTS
from rules.board import Board
from rules.grid import cell_name
from rules.stats import BattleStats


class Game:
    def __init__(self, options=None):
        self.options = {"bomb": True, "repair": True, "shield": True}
        self.options.update(options or {})
        self.boards = [Board(), Board()]
        self.names = ["Player 1", "Player 2"]
        self.current = 0
        self.attacks_left = 0       # > 0 while the player is mid-turn (Frigate / Submarine)
        self.winner = None
        self.difficulty = "intermediate"   # NEW LINE: "beginner" | "intermediate" | "expert"
        self.log = []               # every line, whole game
        self.turn_log = []          # lines from the turn in progress
        self.last_turn_log = []     # lines from the turn that just ended
        self.stats = None           # BattleStats, created once the battle begins

    @property
    def me(self):
        return self.boards[self.current]

    @property
    def foe(self):
        return self.boards[1 - self.current]

    def begin(self):
        """Call once both boards are set up."""
        self.current = 0
        self.winner = None
        self.stats = BattleStats(self.names)
        self._start_turn()

    # ----- turn flow -----
    def _start_turn(self):
        self.attacks_left = 0
        for ship in self.me.ships:
            ship.ability.tick()
            ship.stealth_left = max(0, ship.stealth_left - 1)

    def end_turn(self):
        if self.stats:
            self.stats.record_turn()
        self.last_turn_log, self.turn_log = self.turn_log, []
        self.current = 1 - self.current
        self._start_turn()

    def _after_action(self):
        for p in (0, 1):
            if self.boards[p].fleet_sunk():
                self.winner = 1 - p
        if self.winner is not None and self.stats:
            self.stats.finish()
        if self.winner is None and self.attacks_left == 0:
            self.end_turn()

    def _finish(self, text):
        """Log the action, check for victory, end the turn unless shots are still owed."""
        line = self._say(text)
        self._after_action()
        return line

    def _say(self, text):
        line = f"{self.names[self.current]} {text}"
        self.log.append(line)
        self.turn_log.append(line)
        return line

    def _start_check(self):
        if self.winner is not None:
            return "The game is over."
        if self.attacks_left > 0:
            return "Finish your shots first."
        return None

    # ----- attack -----
    def attack(self, cell):
        if self.winner is not None:
            return False, "The game is over."
        if not self.foe.can_fire(cell):
            return False, "You can't fire there."
        if self.attacks_left == 0:              # a plain one-shot turn
            self.attacks_left = 1
        self.attacks_left -= 1
        return True, self._finish(self._shoot(cell))

    def _shoot(self, cell):
        attacker = self.current
        result, ship = self.foe.receive_attack(cell)
        where = cell_name(cell)

        if self.stats:
            self.stats.record_shot(attacker, result, bool(ship and ship.sunk))

        if result == "hit":
            return f"fires at {where}: HIT" + (f" - {ship.name} SUNK!" if ship.sunk else "")

        if result == "blocked":
            return f"fires at {where}: a shield blocked the hit"

        if result == "stealth":
            return f"fires at {where}: SUBMARINE DETECTED - no damage"

        if result == "bomb":
            return f"fires at {where}: BOMB! " + extras.detonate_bomb(self.me)

        return f"fires at {where}: miss"

    # ----- ship abilities -----
    def use_ability(self, ship_name, target=None):
        """
        target depends on the ability:
          recon -> (row, col) cell    row_scan -> row index    relocate -> list of new cells
          barrage_attacks / stealth -> None
        """
        err = self._start_check()
        if err:
            return False, err
        ship = self.me.get_ship(ship_name)
        if ship is None or ship.sunk:
            return False, f"{ship_name} is not in action."
        ability = ship.ability
        if not ability.ready:
            return False, f"{ability.label} isn't ready."

        error, text = ABILITY_EFFECTS[ability.key](self, ship, target)
        if error:
            return False, error
        ability.spend()
        if self.stats:
            self.stats.record_ability(self.current, ability.label)
        return True, self._finish(text)

    # ----- optional mechanics -----
    def use_repair(self, cell):
        return self._use_extra(extras.repair, cell, self.stats.record_repair if self.stats else None)

    def use_shield(self, cell):
        return self._use_extra(extras.shield, cell, self.stats.record_shield if self.stats else None)

    def _use_extra(self, effect, cell, record=None):
        err = self._start_check()
        if err:
            return False, err
        error, text = effect(self, cell)
        if error:
            return False, error
        if record:
            record(self.current)
        return True, self._finish(text)
