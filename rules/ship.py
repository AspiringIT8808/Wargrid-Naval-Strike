"""A ship: its cells, damage, shields, stealth flag and its one ability."""
from rules.abilities import Ability


class Ship:
    def __init__(self, spec, cells):
        self.name = spec["name"]
        self.size = spec["size"]
        self.cells = list(cells)          # cells[i] is segment i
        self.hit = set()                  # damaged segment indices
        self.shield = set()               # shielded segment indices
        self.stealth_left = 0             # > 0 -> untargetable
        self.ability = Ability(spec)

    @property
    def hp(self):
        return self.size - len(self.hit)

    @property
    def sunk(self):
        return self.hp == 0

    @property
    def stealthed(self):
        return self.stealth_left > 0
