# WARGRID: Naval Strike — Rules

## 1. Game Overview

**WARGRID: Naval Strike** is a tactical Battleship game played on a **15 × 15 grid**.

Each player commands a fleet of five ships. Players take turns attacking the opposing board while using ship-specific abilities and additional tactical actions.

The game supports:

* Player vs Computer
* Two-player local hot-seat play
* Beginner, Intermediate, and Expert AI
* Optional Bomb, Repair, and Shield mechanics

The objective is to **sink the opposing player's entire fleet**.

---

# 2. Board

Each player has a **15 × 15 grid**.

Coordinates use letters for columns and numbers for rows:

```text
    A B C D E F G H I J K L M N O
 1  . . . . . . . . . . . . . . .
 2  . . . . . . . . . . . . . . .
 3  . . . . . . . . . . . . . . .
...
15  . . . . . . . . . . . . . . .
```

A cell is identified using its column and row, such as:

* A1
* H7
* O15

Ships occupy consecutive cells horizontally or vertically.

Ships **may touch each other**, including diagonally.

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

A ship is **sunk** when every segment belonging to it has been hit.

The game ends when one player's entire fleet has been sunk.

---

# 4. Normal Attacks

A normal attack targets one cell on the opponent's board.

Possible results include:

### Miss

The selected cell contains no ship.

The cell is recorded as having been fired upon.

### Hit

The selected cell contains an active ship segment.

That segment becomes damaged.

### Shielded Hit

The selected cell contains a shielded ship segment.

The shield is destroyed, but the ship segment is **not damaged**.

### Stealth

If the targeted ship is currently stealthed, the attack does not damage it.

A normal attack normally gives the player one shot for the turn.

---

# 5. Ship Abilities

Each ship has its own special ability.

Abilities have a limited number of uses.

An ability can only be used while its ship is still operational and its ability is available.

## 5.1 Frigate — BARRAGE ATTACK

The Frigate replaces its normal attack with a barrage.

The player receives **four attacks during the turn**.

Each attack is resolved normally and can independently result in a miss, hit, shield block, or other applicable result.

**Uses:** 3

The ability is intended to make the Frigate the fleet's primary offensive ship.

---

## 5.2 Destroyer — RELOCATE

The Destroyer may move to a new legal position on its board.

The new position:

* Must remain within the board.
* Must preserve the Destroyer's size.
* Must not overlap another ship.
* Must not occupy bombed cells.
* Must be different from its current position.
* Must not contain cells that have already been fired upon.

The Destroyer's existing damage is retained when it relocates.

**Uses:** 1

---

## 5.3 Carrier — RECON

The Carrier scans a **3 × 3 area** centered on a selected enemy cell.

The scan reveals information about the selected area without directly damaging ships.

Areas extending beyond the edge of the board are clipped to the board.

**Uses:** 2

---

## 5.4 Cruiser — ROW SCAN

The Cruiser scans an entire row of the enemy board.

The player selects a row from 1–15.

All cells in that row are scanned.

**Uses:** 2

---

## 5.5 Submarine — STEALTH

The Submarine becomes untargetable for **three rounds**.

During Stealth, attacks against the Submarine cannot damage it.

Using Stealth also gives the player one attack during that turn.

**Uses:** 1

---

# 6. Repair

Repair is an optional game mechanic.

When available, a player may repair one damaged ship segment.

A repaired segment:

* No longer counts as damaged.
* Can be attacked again.
* Has its corresponding previous hit removed from the board's recorded shots.

Repair therefore restores the segment to a state where it can receive damage again.

A player has **three Repair uses** by default.

---

# 7. Shield

Shield is an optional game mechanic.

A player may place a shield on an undamaged ship segment.

When that segment is attacked:

1. The shield is consumed.
2. The segment is not damaged.

A shield does not prevent other effects that specifically ignore shields.

A player has **three Shield uses** by default.

---

# 8. Bomb

Bomb is an optional game mechanic.

The Bomb is placed during deployment.

A bomb does not directly attack the opponent.

Instead, when triggered, it damages the **attacker's own fleet**.

The Bomb:

* Targets the attacker's healthiest remaining ship.
* Selects one currently undamaged segment of that ship.
* Damages that segment.
* Ignores shields.

The Bomb therefore acts as a hazardous area on the board rather than an offensive weapon.

---

# 9. Turn System

Players alternate turns.

At the beginning of a turn:

* The player's attack count is reset.
* Ability cooldowns, if applicable, are updated.
* Active Stealth durations are reduced.

A normal attack consumes the player's available attack.

Abilities may modify the number of attacks available during the turn.

For example:

```text
Normal Turn
→ 1 attack

Barrage
→ 4 attacks
```

A turn ends when the player has no attacks remaining or when the game determines that the action sequence is complete.

If a fleet has been completely sunk, the game ends immediately instead of continuing to the next player.

---

# 10. Victory

A player wins when every ship belonging to the opposing player has been sunk.

In two-player hot-seat mode, the game-over screen prevents the defeated player's board information from being immediately exposed before the device is handed to the other player.

---

# 11. AI Difficulty

The AI has three difficulty levels.

## Beginner

Beginner AI is designed to teach the fundamentals of Battleship.

It primarily selects legal random shots and does not make sophisticated use of abilities.

The purpose is to allow a new player to learn:

* Grid coordinates
* Hit and miss behavior
* Ship placement
* Basic attacking
* Fleet destruction

---

## Intermediate

Intermediate AI introduces tactical play.

It can:

* Track successful hits.
* Hunt damaged ships.
* Select follow-up targets.
* Use basic ability strategies.
* Take advantage of information obtained during the game.

The purpose is to teach the player to fight against an opponent that understands both the basic Battleship rules and the game's special abilities.

---

## Expert

Expert AI uses more advanced tactical reasoning.

It can use:

* Probability-based target selection
* Remaining ship sizes
* Hit tracking
* Target chasing
* Recon
* Row Scan
* Relocation
* Stealth
* Repair
* Shield
* Other available tactical information

Expert AI is intended to expose the player to the full tactical system rather than simply increasing the randomness or number of attacks.

---

# 12. Information and Scanning

The game maintains information about cells that have been attacked or scanned.

Attacked cells cannot normally be attacked again.

Scanning provides information without functioning as a normal attack.

Different scanning abilities provide different amounts of information:

* **Recon:** 3 × 3 area
* **Row Scan:** entire row

Scanned information remains part of the player's available tactical information.

---

# 13. Deployment

Before battle, each player deploys their fleet.

Ships must:

* Fit entirely inside the 15 × 15 board.
* Occupy the correct number of cells for their size.
* Not overlap another ship.
* Not occupy a bombed cell.

Ships may be placed horizontally or vertically.

The player may manually position ships or use randomized deployment.

---

# 14. Rules Architecture

The project separates the game rules from the graphical interface.

```text
rules/
    game.py
    board.py
    ship.py
    abilities.py
    ai.py
    ai_beginner.py
    ai_intermediate.py
    ai_expert.py
    grid.py
    extras.py
    config.py
```

The `rules/` package contains the actual game logic and does not depend on Pygame.

The UI communicates with the rules through game actions such as:

```text
Game.attack()
Game.use_ability()
Game.use_repair()
Game.use_shield()
```

The intended architecture is:

> **Rules decide. UI shows.**

This allows the game mechanics and AI to operate independently from the graphical presentation.

---

# 15. Default Configuration

Current default configuration:

```text
Grid: 15 × 15

Frigate:
    Size: 5
    Barrage uses: 3

Destroyer:
    Size: 3
    Relocate uses: 1

Carrier:
    Size: 3
    Recon uses: 2

Cruiser:
    Size: 2
    Row Scan uses: 2

Submarine:
    Size: 2
    Stealth uses: 1
    Stealth duration: 3 rounds

Repair uses: 3
Shield uses: 3
Recon area: 3 × 3
```

Optional mechanics can be enabled or disabled through the game's configuration.

---

# 16. Design Philosophy

WARGRID: Naval Strike is designed around progressively teaching tactical Battleship.

The three AI levels represent different stages of play:

```text
BEGINNER
Learn Battleship
        ↓
INTERMEDIATE
Learn to fight tactical opponents
        ↓
EXPERT
Learn advanced tactical decision-making
```

The goal is not simply to make the AI increasingly difficult.

The goal is to make the player progressively understand the game's systems.
