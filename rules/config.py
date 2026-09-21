"""
TUNING KNOBS. Change numbers here to rebalance the game; no other file needs to change.

  uses      total uses per game (None = unlimited)
  cooldown  rounds before it can be used again (0 = never recharges).
            Used on your turn N with cooldown 2 -> ready again on your turn N+2.
"""

GRID = 15

SHIP_SPECS = [
    # Frigate option B (rechargeable): uses=None, cooldown=2
    dict(name="Frigate",   size=5, key="barrage_attacks", label="BARRAGE ATTACK", uses=3, cooldown=0),
    # Destroyer: one-time now; set cooldown=N (and uses=None) to let it recharge
    dict(name="Destroyer", size=3, key="relocate",      label="RELOCATE",      uses=1, cooldown=0),
    # Carrier option B (rechargeable): uses=None, cooldown=2 and RECON_SIZE = 2
    dict(name="Carrier",   size=3, key="recon",         label="RECON",         uses=2, cooldown=0),
    # Cruiser: "once or twice" -> change uses
    dict(name="Cruiser",   size=2, key="row_scan",      label="ROW SCAN",      uses=2, cooldown=0),
    dict(name="Submarine", size=2, key="stealth",       label="STEALTH",       uses=1, cooldown=0),
]

RECON_SIZE = 3        # 3 = 3x3 reveal (2 = 2x2, where the clicked cell is the top-left)
STEALTH_ROUNDS = 3    # how many enemy turns the Submarine is untargetable
REPAIR_USES = 3
SHIELD_USES = 3

# Lookups built from SHIP_SPECS (don't edit)
SPEC_BY_NAME = {s["name"]: s for s in SHIP_SPECS}
SHIP_BY_KEY = {s["key"]: s["name"] for s in SHIP_SPECS}      # ability key -> ship name
