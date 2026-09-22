# WARGRID: Naval Strike — Rules

## 1. Game Overview

**WARGRID: Naval Strike** is a tactical Battleship game played on a **15 × 15 grid**.

Each player commands a fleet of five ships.

Players alternate turns, attacking the opposing board while using ship-specific abilities and, when enabled, the optional Bomb, Repair, and Shield mechanics.

The game supports:

* Player vs Computer
* Two-player local hot-seat play
* Beginner AI
* Intermediate AI
* Expert AI
* Optional Bomb
* Optional Repair
* Optional Shield

The objective is to **sink the opposing player's entire fleet**.

---

# 2. Board

Each player has a:

```text
15 × 15
```

grid.

Columns are represented by letters:

```text
A B C D E F G H I J K L M N O
```

Rows are numbered:

```text
1–15
```

Example coordinates:

```text
A1
H7
O15
```

A board therefore contains 225 cells.

Ships occupy consecutive cells horizontally or vertically.

Ships **may touch one another**, including diagonally.

---

# 3. Fleet

Each player has five ships.

| Ship      | Size | Ability        | Uses |
| --------- | ---: | -------------- | ---: |
| Frigate   |    5 | Barrage Attack |    3 |
| Destroyer |    3 | Relocate       |    1 |
| Carrier   |    3 | Recon          |    2 |
| Cruiser   |    2 | Row Scan       |    2 |
| Submarine |    2 | Stealth        |    1 |

The total fleet size is:

```text
5 + 3 + 3 + 2 + 2 = 15 segments
```

A ship is **sunk** when all of its segments are damaged.

A player loses when every ship in their fleet is sunk.

---

# 4. Fleet Deployment

Before the battle begins, each player must deploy all five ships.

Ships must:

* Remain inside the board
* Occupy the correct number of cells
* Use consecutive horizontal or vertical cells
* Not overlap another ship
* Not occupy the Bomb cell when Bomb is enabled

Ships are allowed to touch.

There is no rule requiring a gap between ships.

---

## 4.1 Manual Deployment

The player selects a ship and clicks a starting cell.

The ship is previewed in the current orientation.

Orientation can be changed using:

```text
R
```

or:

```text
Right Mouse Button
```

A placed ship can be clicked again to pick it up and reposition it.

---

## 4.2 Random Deployment

The setup screen provides:

```text
RANDOMIZE ALL
```

Random deployment generates legal positions for every ship.

If Bomb is enabled, the Bomb is also placed on an open-water cell.

---

## 4.3 Ready State

A player can only finish deployment when:

* All five ships have been placed.
* If Bomb is enabled, a Bomb has also been placed.

---

# 5. Normal Attacks

A normal attack targets one cell on the opponent's board.

The target must be a legal fireable cell.

Normally, a player receives:

```text
1 attack
```

for a turn.

The following results are possible.

---

## 5.1 Miss

If the selected cell contains no ship:

```text
MISS
```

The cell is recorded as a miss.

The cell cannot normally be fired at again.

---

## 5.2 Hit

If the selected cell contains an active ship segment:

```text
HIT
```

The corresponding ship segment becomes damaged.

If all segments of that ship are damaged, the ship is reported as sunk.

---

## 5.3 Shield Block

If the selected ship segment has a shield:

1. The shield is removed.
2. The segment is not damaged.
3. The shot is recorded as:

```text
blocked
```

Because the shield has been consumed, the same cell can be targeted again.

---

## 5.4 Stealth

If the selected cell belongs to a ship that is currently stealthed:

```text
SUBMARINE DETECTED - no damage
```

The attack does not damage the ship.

The stealth state remains active until its duration expires.

---

## 5.5 Bomb

If the selected cell contains a hidden Bomb:

1. The Bomb is triggered.
2. The Bomb is removed.
3. The attacker's own fleet is damaged.

The Bomb therefore does not damage the board being fired upon.

---

# 6. Ship Abilities

Each ship has one unique ability.

Ability uses are tracked separately for each ship.

An ability is available only when:

* The ship is still operational.
* The ability has remaining uses.
* Its cooldown, if configured, has expired.

The current configuration uses limited total uses and zero cooldown for all five abilities.

The shared ability system supports cooldowns, so this can be changed in `rules/config.py`.

---

# 7. Frigate — BARRAGE ATTACK

The Frigate can replace its normal attack with a four-shot barrage.

When activated:

```text
attacks_left = 4
```

The player may therefore make four attacks during that turn.

Each attack is independently resolved.

Possible results include:

* Miss
* Hit
* Shield block
* Stealth
* Bomb

The ability consumes one Frigate use.

**Uses:** 3

### Important

Barrage currently gives **four attacks**, not two.

The four attacks are implemented directly by the game rules.

---

# 8. Destroyer — RELOCATE

The Destroyer can move to a new position on its own board.

The new position must:

* Contain exactly three cells
* Remain inside the board
* Be horizontal or vertical
* Not overlap another ship
* Not occupy the Bomb cell
* Be different from the current position
* Not contain cells that have already been fired upon by the opponent

The Destroyer's current damage remains attached to the ship.

Its shields also remain attached to their corresponding ship segments.

Therefore, relocation moves the ship rather than creating a new undamaged Destroyer.

**Uses:** 1

---

# 9. Carrier — RECON

The Carrier can scan an area of the enemy board.

The current configuration is:

```text
RECON_SIZE = 3
```

Therefore, Recon scans a:

```text
3 × 3
```

area centered on the selected cell.

The scan does not directly damage ships.

Instead, each scanned cell records whether a ship was present at the time of the scan.

Areas extending beyond the edge of the board are clipped to valid board cells.

**Uses:** 2

---

# 10. Cruiser — ROW SCAN

The Cruiser can scan an entire enemy row.

The player selects a row from:

```text
1–15
```

All cells in that row are scanned.

The scan records whether each cell contained a ship at the time it was scanned.

The scan does not directly damage ships.

**Uses:** 2

---

# 11. Submarine — STEALTH

The Submarine can temporarily become untargetable.

When activated:

```text
STEALTH_ROUNDS = 3
```

The Submarine cannot be damaged by attacks while its stealth duration is active.

Stealth lasts for **three enemy turns**.

The Submarine also receives one attack during the turn in which Stealth is activated.

Therefore:

```text
Stealth
    +
1 attack
```

is possible in the same turn.

This is the only ability that explicitly provides an attack in addition to the ability.

**Uses:** 1

---

# 12. Repair

Repair is an optional mechanic.

It can be enabled or disabled from the main menu.

When enabled, a player may repair one damaged segment belonging to a ship that has not yet sunk.

The selected cell must:

* Belong to a ship
* Be damaged
* Belong to a ship that is still afloat

When repaired:

1. The segment is removed from the ship's damaged set.
2. The corresponding `"hit"` entry is removed from the board's shot history.
3. The opponent can therefore fire at the cell again.

The repaired segment is not permanently protected.

It can be damaged again by a future attack.

**Default uses:** 3

---

# 13. Shield

Shield is an optional mechanic.

It can be enabled or disabled from the main menu.

A Shield can be placed on an undamaged ship segment.

The selected cell must:

* Belong to a ship
* Not already be damaged
* Not already have a shield
* Belong to a ship that is still afloat

When the protected segment is attacked:

1. The shield is consumed.
2. The segment remains undamaged.
3. The shot is recorded as blocked.

Because the shield is consumed, the attacker may target the cell again.

**Default uses:** 3

---

# 14. Bomb

Bomb is an optional mechanic.

It can be enabled or disabled from the main menu.

The Bomb is placed during deployment.

The Bomb must:

* Be inside the board
* Be placed on open water
* Not occupy a ship's cell

The Bomb remains hidden from the opponent.

When the opponent fires at the Bomb:

1. The Bomb triggers.
2. The Bomb is removed.
3. The attacker's surviving ships are examined.
4. The ship with the highest remaining HP is selected.
5. One currently undamaged segment is selected.
6. That segment takes one damage.
7. Any shield on that segment is removed/ignored.

If multiple surviving ships have the same highest HP, the affected ship is selected randomly.

The Bomb can therefore damage the attacker even though the attack was made against an apparently empty enemy cell.

---

# 15. Turn System

Players alternate turns.

At the beginning of each turn:

1. The player's `attacks_left` value is reset.
2. Ability cooldowns are updated.
3. Active Stealth durations for the current player's ships are updated.

A normal attack starts a one-shot turn if no special ability has already assigned additional attacks.

---

## 15.1 Normal Turn

A normal turn provides:

```text
1 attack
```

The player fires once.

The turn then passes to the opponent unless the game has ended.

---

## 15.2 Barrage Turn

When the Frigate uses Barrage:

```text
4 attacks
```

remain available.

The player can continue attacking until all four attacks have been used.

The turn ends after the final attack unless the game ends earlier.

---

## 15.3 Stealth Turn

When the Submarine uses Stealth:

```text
Stealth activated
+
1 attack
```

The player can immediately make one attack.

After that attack, the turn ends unless the game has already ended.

---

## 15.4 Other Abilities

Recon, Row Scan, and Relocate consume the player's action.

The turn ends after the ability resolves.

Repair and Shield also consume the player's action.

The general rule is:

```text
One action per turn
```

with the explicit exceptions of:

```text
Barrage → 4 attacks
Stealth → Stealth + 1 attack
```

---

# 16. Ability Cooldowns

The ability system supports both uses and cooldowns.

Each ability has:

```text
uses
cooldown
```

in `rules/config.py`.

Current configuration:

| Ship      | Uses | Cooldown |
| --------- | ---: | -------: |
| Frigate   |    3 |        0 |
| Destroyer |    1 |        0 |
| Carrier   |    2 |        0 |
| Cruiser   |    2 |        0 |
| Submarine |    1 |        0 |

A cooldown of zero means the ability does not wait for a future turn after being used.

The `Ability` class supports cooldowns if they are introduced later.

---

# 17. Victory

A player wins when the opponent's entire fleet is sunk.

The game checks the fleets after actions.

If all ships belonging to one player are sunk:

```text
winner
```

is set immediately.

The game does not continue to another turn after the fleet has been completely destroyed.

---

# 18. Two-Player Hot-Seat Mode

Two-player mode uses the same computer for both players.

The setup flow is:

```text
Player 1 deployment
        ↓
Handoff
        ↓
Player 2 deployment
        ↓
Handoff
        ↓
Player 1 starts
```

During the battle, players alternate turns.

The handoff screen is used to prevent the next player from immediately seeing information belonging to the previous player.

---

# 19. Player vs Computer Mode

When playing against the computer:

1. The human player deploys their fleet.
2. The computer automatically receives a randomized legal fleet.
3. Player 1 begins the battle.

The selected AI difficulty determines which computer module controls the opponent.

---

# 20. AI System

The AI is divided into three implementations.

```text
rules/ai.py
        │
        ├── ai_beginner.py
        ├── ai_intermediate.py
        └── ai_expert.py
```

`rules/ai.py` selects the appropriate implementation based on:

```python
game.difficulty
```

Supported values:

```text
beginner
intermediate
expert
```

The default difficulty is:

```text
intermediate
```

---

# 21. Beginner AI

The Beginner AI selects a random legal cell.

It does not:

* Hunt damaged ships
* Follow up on hits
* Read scan information
* Use ship abilities

Its core behavior is:

```text
Find legal cells
        ↓
Choose one randomly
        ↓
Attack
```

---

# 22. Intermediate AI

The Intermediate AI introduces basic tactical behavior.

It maintains a hunt/target system.

If a previous attack has:

* Hit an unsunk ship, or
* Been blocked by a shield

the AI prioritizes relevant nearby cells.

If there are no immediate targets, it uses a checkerboard-style search pattern where possible.

The Intermediate AI can also use:

### Frigate

Barrage is more likely to be used when the AI already has a target to chase.

### Submarine

Stealth becomes more likely when the AI's own fleet has multiple damaged ships.

The Intermediate AI does not strategically use every ability.

---

# 23. Expert AI

The Expert AI uses a more complete tactical system.

Its targeting priorities include:

1. A cell whose shield has just blocked an attack
2. A ship location revealed by Recon or Row Scan
3. Confirmed hits that can be extended into a line
4. Probability-density targeting
5. Random legal targeting as a fallback

---

## 23.1 Shield-Block Targeting

When a shield blocks a shot, the AI knows that:

* A ship is present
* The shield has already been consumed

The blocked cell becomes a high-priority target.

---

## 23.2 Scan Targeting

If Recon or Row Scan has revealed that a ship is present in a cell, the AI can prioritize that cell.

---

## 23.3 Hit-Line Targeting

When multiple unsunk hits belong to the same ship and form a horizontal or vertical line, the Expert AI attempts to extend that line toward the ship's remaining cells.

---

## 23.4 Probability-Density Targeting

When there is no immediate target, the Expert AI builds a probability map.

It considers:

* Remaining ship sizes
* Known misses
* Known Bomb cells
* Cells that can still legally be fired upon
* Possible horizontal ship placements
* Possible vertical ship placements

Each possible placement contributes to the score of the cells it covers.

The AI then targets cells with the highest resulting score.

---

# 24. Expert AI Abilities

The Expert AI can use the fleet's abilities strategically.

---

## 24.1 Frigate

Barrage is prioritized when the AI is actively chasing a target.

The additional attacks are used to capitalize on information the AI already has.

---

## 24.2 Destroyer

The Expert AI can relocate a damaged Destroyer.

It searches for a legal location that:

* Preserves ship size
* Avoids overlap
* Avoids the Bomb
* Avoids cells already fired upon

The purpose is to move a known damaged ship away from exposed cells.

---

## 24.3 Carrier

Recon is considered when there is no active target.

The Expert AI chooses a scan center using its probability-density information.

---

## 24.4 Cruiser

Row Scan is considered when there is no active target.

The AI chooses a row using the probability information available to it.

---

## 24.5 Submarine

Stealth becomes more likely when the AI's own fleet has multiple damaged ships.

The AI can therefore protect its Submarine while still receiving one attack during the Stealth turn.

---

## 24.6 Repair

The Expert AI can use Repair when it has no active hunt.

It selects a damaged cell from a surviving ship.

The largest damaged ship is prioritized.

---

## 24.7 Shield

The Expert AI can use Shield when it has no active hunt.

It selects an undamaged, unshielded cell from a surviving ship.

The largest available ship is prioritized.

---

# 25. Game State

The central game object is:

```python
rules.game.Game
```

It owns the overall match state.

Important state includes:

```text
options
boards
names
current player
attacks_left
winner
difficulty
log
turn_log
last_turn_log
```

The two player boards are stored in:

```python
game.boards
```

The active player's board is exposed through:

```python
game.me
```

The opponent's board is exposed through:

```python
game.foe
```

---

# 26. Action Interface

The UI communicates with the rules system primarily through:

```python
game.attack(cell)
game.use_ability(ship_name, target)
game.use_repair(cell)
game.use_shield(cell)
```

Each action returns:

```text
(ok, text)
```

where:

* `ok = False` means the action was rejected.
* `ok = True` means the action was applied.
* `text` describes the result.

Invalid actions do not modify the game state.

---

# 27. Board State

Each `Board` tracks:

```text
ships
shots
scanned
bomb
repairs_left
shields_left
```

### `ships`

The player's fleet.

### `shots`

Cells that have been fired upon.

Possible values include:

```text
hit
miss
blocked
bomb
```

### `scanned`

Cells whose ship presence has been revealed through Recon or Row Scan.

### `bomb`

The current hidden Bomb cell, if Bomb is enabled.

### `repairs_left`

Remaining Repair uses.

### `shields_left`

Remaining Shield uses.

---

# 28. Ship State

Each ship tracks:

```text
name
size
cells
hit
shield
stealth_left
ability
```

The ship's remaining HP is calculated as:

```text
size - number of damaged segments
```

A ship is sunk when its HP reaches zero.

---

# 29. Configuration

Most balancing values are centralized in:

```text
rules/config.py
```

Current values:

```python
GRID = 15

RECON_SIZE = 3
STEALTH_ROUNDS = 3

REPAIR_USES = 3
SHIELD_USES = 3
```

Current fleet configuration:

```text
Frigate     size 5   Barrage Attack   3 uses
Destroyer   size 3   Relocate         1 use
Carrier     size 3   Recon            2 uses
Cruiser     size 2   Row Scan         2 uses
Submarine   size 2   Stealth          1 use
```

---

# 30. Optional Mechanics Configuration

The main application currently starts with:

```python
{
    "bomb": True,
    "repair": True,
    "shield": True
}
```

Each mechanic can then be toggled from the main menu.

The selected options are passed into the `Game`.

---

# 31. Architecture

The project follows a separation between rules and presentation.

```text
                    ┌──────────────────┐
                    │       UI         │
                    │      ui/         │
                    └────────┬─────────┘
                             │
                             │ actions
                             ▼
                    ┌──────────────────┐
                    │      Game        │
                    │   rules/game.py  │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     ┌─────────┐       ┌───────────┐      ┌─────────┐
     │  Board  │       │ Abilities │      │ Extras  │
     │ board.py│       │abilities.py│     │extras.py│
     └─────────┘       └───────────┘      └─────────┘
          │
          ▼
      ┌─────────┐
      │  Ship   │
      │ ship.py │
      └─────────┘
```

The guiding rule is:

> **`rules/` decides, `ui/` shows.**

The UI should not directly manipulate ship damage, board shots, ability uses, or victory state.

It should request an action from `Game` and display the result.

---

# 32. File Responsibilities

## `rules/config.py`

Central tuning values.

## `rules/grid.py`

Grid coordinates and cell-generation helpers.

## `rules/abilities.py`

Ability bookkeeping and ability effects.

## `rules/ship.py`

Ship state.

## `rules/board.py`

Board state, placement, attacks, scans, movement validation, Repair/Shield helpers.

## `rules/extras.py`

Bomb, Repair, and Shield behavior.

## `rules/game.py`

Turn flow and public game actions.

## `rules/ai.py`

AI difficulty dispatcher.

## `rules/ai_beginner.py`

Beginner AI.

## `rules/ai_intermediate.py`

Intermediate AI.

## `rules/ai_expert.py`

Expert AI.

---

# 33. UI Flow

The application uses the following screen flow:

```text
MENU
  ↓
SETUP
  ↓
HANDOFF (two-player mode)
  ↓
PLAY
  ↓
GAME OVER
```

The main application is managed by:

```text
ui/app.py
```

---

# 34. Audio

The audio system is separated from the rules system.

```text
audio/music.py
audio/sound_manager.py
audio/sfx.py
```

The current implementation provides background music through `MusicPlayer`.

The application also provides a mute toggle.

Music is started when the application starts and stopped when the application exits.

---

# 35. Current Default Game

Unless changed from the menu, the game starts with:

```text
Board:
15 × 15

Mode:
Player vs Computer

AI:
Intermediate

Bomb:
ON

Repair:
ON

Shield:
ON
```

The default difficulty is defined by the application as:

```text
intermediate
```

---

# 36. Quick Rules Reference

```text
BOARD
15 × 15

FLEET
Frigate       5
Destroyer     3
Carrier       3
Cruiser       2
Submarine     2

ABILITIES
Frigate       Barrage       4 attacks
Destroyer     Relocate      move ship
Carrier       Recon         3 × 3 scan
Cruiser       Row Scan      scan one row
Submarine     Stealth       3 enemy turns + 1 attack

DEFAULT USES
Barrage       3
Relocate      1
Recon         2
Row Scan      2
Stealth       1

OPTIONAL
Bomb          1 hidden trap
Repair        3 uses
Shield        3 uses

NORMAL TURN
1 attack

SPECIAL TURNS
Barrage       4 attacks
Stealth       stealth + 1 attack

VICTORY
Sink the entire enemy fleet
```

---

# 37. Rule of the House

When modifying the project:

> **Put game rules in `rules/`. Put presentation in `ui/`.**

If a change determines **what is legal, what happens, how damage works, how turns work, or how the AI decides**, it belongs in the rules layer.

If a change determines **what the player sees, clicks, hears, or how the interface is arranged**, it belongs in the UI/audio layer.

For balance changes, start with:

```text
rules/config.py
```
