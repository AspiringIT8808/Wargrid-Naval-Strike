# WARGRID: Naval Strike

A tactical Battleship game built with Python and Pygame.

**WARGRID: Naval Strike** expands the classic Battleship formula with a 15×15 battlefield, ship-specific abilities, optional tactical mechanics, multiple AI difficulties, local two-player play, and a dedicated Pygame interface.

---

## Features

* 15×15 tactical game board
* Player vs Computer
* 2-player local hot-seat mode
* Three computer difficulty levels:

  * Beginner
  * Intermediate
  * Expert
* Five ships with unique abilities
* Optional:

  * Bomb
  * Repair
  * Shield
* Fleet deployment with manual placement
* Random fleet deployment
* Ship relocation
* Recon and row scanning
* Submarine stealth
* Turn-based attack system
* Battle log
* Fleet status display
* Background music
* In-game mute control
* Separate game rules and UI layers

---

# Requirements

## Python Version

This project is developed and tested with:

```text
Python 3.12
```

**Python 3.14 is not recommended for this project** because Pygame may not yet provide a compatible package for every Python 3.14/platform combination. This can cause `pip install pygame` to fail.

For the most reliable setup, use **Python 3.12**.

---

## Dependencies

The project currently requires:

```text
pygame
```

All Python dependencies are listed in:

```text
requirements.txt
```

Install them with:

```bash
python -m pip install -r requirements.txt
```

Using `python -m pip` is recommended instead of calling `pip` directly because it makes it clearer which Python installation is receiving the package.

---

# Installation

## 1. Check Your Python Version

Run:

```bash
python --version
```

You should see something similar to:

```text
Python 3.12.x
```

On Windows, you can also use:

```bash
py --version
```

---

## 2. Create a Virtual Environment

Creating a virtual environment is recommended so that the project's packages do not interfere with other Python projects.

On Windows:

```bash
py -3.12 -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

## 3. Install Dependencies

With the virtual environment activated:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 4. Run the Game

```bash
python main.py
```

On Windows, this also works when Python 3.12 is installed:

```bash
py -3.12 main.py
```

---

# If Pygame Will Not Install

If you see an error while running:

```bash
python -m pip install pygame
```

first check your Python version:

```bash
python --version
```

If you are using Python 3.14, install **Python 3.12** and create the project's virtual environment with it.

For example:

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

Do not change the project's source code to work around a Pygame installation failure until the Python/Pygame installation itself has been checked.

---

# How to Play

## 1. Choose Game Options

From the main menu you can choose:

### Game Mode

**PLAY VS COMPUTER**

Play against the selected AI difficulty.

**2 PLAYERS - ONE SCREEN**

Play locally against another player using the same computer.

A handoff screen is used between players so each player can deploy and play without immediately exposing the other player's board.

---

## 2. Choose AI Difficulty

When playing against the computer, select one of:

### Beginner

The computer fires at random legal cells.

It does not:

* Hunt damaged ships
* Follow up on hits
* Read scan information
* Use ship abilities

This is the simplest opponent.

### Intermediate

The computer introduces basic tactical behavior.

It can:

* Follow up on successful hits
* Hunt damaged ships
* Use checkerboard-style searching when hunting is not active
* Use Frigate Barrage strategically
* Use Submarine Stealth when its fleet is taking damage

It does not make full strategic use of every ship ability.

### Expert

The computer uses the complete tactical system.

It can make use of:

* Hit tracking
* Shield-block information
* Scan information
* Hit-line targeting
* Probability-density targeting
* Barrage
* Relocate
* Recon
* Row Scan
* Stealth
* Repair
* Shield

The Expert AI also considers remaining ship sizes when calculating likely target locations.

---

# Fleet

Each player controls five ships.

| Ship      | Size | Ability        | Uses |
| --------- | ---: | -------------- | ---: |
| Frigate   |    5 | Barrage Attack |    3 |
| Destroyer |    3 | Relocate       |    1 |
| Carrier   |    3 | Recon          |    2 |
| Cruiser   |    2 | Row Scan       |    2 |
| Submarine |    2 | Stealth        |    1 |

A ship is sunk when every segment belonging to it has been damaged.

A player loses when their entire fleet has been sunk.

---

# Ship Abilities

## Frigate — BARRAGE ATTACK

The Frigate replaces its normal attack with a barrage.

The player receives:

```text
4 attacks
```

during that turn.

Each attack is resolved normally.

**Uses:** 3

---

## Destroyer — RELOCATE

The Destroyer can move to a new legal position on its own board.

The new position must:

* Remain inside the board
* Preserve the Destroyer's size
* Not overlap another ship
* Not occupy the Bomb cell
* Be different from its current position
* Not contain cells already fired upon by the opponent

The Destroyer's existing damage and shields remain attached to the ship when it moves.

**Uses:** 1

---

## Carrier — RECON

The Carrier scans a 3×3 area centered around a selected enemy cell.

The scan reveals whether cells contain ships but does not damage them.

Areas extending beyond the board are clipped to the board.

**Uses:** 2

---

## Cruiser — ROW SCAN

The Cruiser scans an entire row of the enemy board.

The player selects a row from 1 to 15.

All cells in that row are revealed through the game's scan information system.

**Uses:** 2

---

## Submarine — STEALTH

The Submarine becomes untargetable for three enemy turns.

During Stealth:

* Attacks against the Submarine do not damage it.
* The Submarine's player still receives one attack when Stealth is activated.

This is the exception to the normal rule that a turn uses either an attack or an ability.

**Uses:** 1

---

# Optional Mechanics

The main menu allows the following mechanics to be enabled or disabled independently.

* Bomb
* Repair
* Shield

---

## Bomb

The Bomb is placed during fleet deployment.

It can only be placed on open water.

The Bomb is a hidden trap rather than a direct attack.

If the opponent fires at the Bomb:

1. The Bomb is triggered.
2. The Bomb is removed.
3. The attacker's healthiest surviving ship is selected.
4. One undamaged segment is damaged.
5. Shields do not protect that segment.

If multiple surviving ships have the same highest HP, one is selected randomly.

---

## Repair

Repair allows a player to restore one damaged segment belonging to a ship that is still afloat.

The repaired segment:

* Is removed from the ship's damaged segments
* Can be attacked again
* Has its previous recorded hit removed from the board's shot history

**Default uses:** 3

---

## Shield

Shield protects one undamaged ship segment.

When that segment is attacked:

1. The shield is consumed.
2. The segment is not damaged.
3. The attack is recorded as blocked.

A blocked cell can be targeted again because the shield has already been consumed.

**Default uses:** 3

---

# Board

Each player has a:

```text
15 × 15
```

board.

Columns use letters:

```text
A B C D E F G H I J K L M N O
```

Rows use numbers:

```text
1–15
```

Examples of valid coordinates:

```text
A1
H7
O15
```

Ships occupy consecutive horizontal or vertical cells.

Ships are allowed to touch one another, including diagonally.

---

# Fleet Deployment

Before the battle begins, each player places all five ships.

Ships can be:

* Placed manually
* Rotated
* Picked up and repositioned
* Randomized using **RANDOMIZE ALL**

Rotation can be performed with:

```text
R
```

or:

```text
Right Mouse Button
```

The player can select a placed ship to pick it up and move it.

If Bomb is enabled, a Bomb must also be placed on an open-water cell before the fleet can be marked ready.

---

# Turn System

Players alternate turns.

A normal turn gives the player:

```text
1 attack
```

Normally, an action is either:

```text
Attack
```

or:

```text
Use one ability
```

The main exceptions are:

### Frigate

Barrage gives:

```text
4 attacks
```

### Submarine

Stealth gives:

```text
Stealth + 1 attack
```

At the start of a player's turn:

* Their attack count is reset.
* Ability cooldowns are updated.
* Their active Stealth duration is updated.

The game checks for victory after actions.

If an entire fleet has been sunk, the game ends immediately.

---

# Attack Results

A normal attack can produce several outcomes.

### Miss

The selected cell contains no ship.

### Hit

The selected cell contains an active ship segment.

The segment becomes damaged.

### Shield Block

The selected cell contains a shielded ship segment.

The shield is consumed, but the segment is not damaged.

### Stealth

The targeted ship is currently stealthed.

The attack does not damage the ship.

### Bomb

The selected cell contains a hidden Bomb.

The Bomb is triggered and damages the attacker's own healthiest surviving ship.

---

# Project Architecture

The project separates game logic from the Pygame interface.

The central rule is:

> **`rules/` decides. `ui/` shows.**

The UI should not directly modify ships, boards, or game state.

Instead, UI screens call methods on `Game`, such as:

```python
game.attack(...)
game.use_ability(...)
game.use_repair(...)
game.use_shield(...)
```

The rules layer resolves the action and returns the result.

This keeps the game logic independent from the visual interface.

---

# Project Structure

```text
battleships/
│
├── main.py
├── README.md
├── requirements.txt
│
├── audio/
│   ├── music.py
│   ├── sfx.py
│   └── sound_manager.py
│
├── docs/
│   └── rules.md
│
├── rules/
│   ├── __init__.py
│   ├── config.py
│   ├── grid.py
│   ├── abilities.py
│   ├── ship.py
│   ├── board.py
│   ├── extras.py
│   ├── game.py
│   │
│   ├── ai.py
│   ├── ai_beginner.py
│   ├── ai_intermediate.py
│   └── ai_expert.py
│
├── settings/
│   └── settings.py
│
└── ui/
    ├── __init__.py
    ├── app.py
    ├── display.py
    ├── theme.py
    ├── layout.py
    ├── widgets.py
    ├── board_view.py
    ├── panels.py
    │
    └── screens/
        ├── __init__.py
        ├── base.py
        ├── menu.py
        ├── setup.py
        ├── handoff.py
        ├── play.py
        └── gameover.py
```

---

# What Each Part Does

## `main.py`

Application entry point.

It creates the Pygame application and starts the main loop.

---

## `rules/config.py`

Central configuration and balancing file.

Contains:

* Board size
* Ship sizes
* Ability names
* Ability uses
* Ability cooldowns
* Recon size
* Stealth duration
* Repair uses
* Shield uses

If you want to rebalance the game, this is usually the first place to look.

---

## `rules/grid.py`

Grid-related helpers.

Handles operations such as:

* Checking board boundaries
* Converting coordinates to names
* Creating horizontal/vertical ship lines
* Creating scan areas

---

## `rules/abilities.py`

Contains the shared ability system and the actual implementation of:

* Barrage Attack
* Relocate
* Recon
* Row Scan
* Stealth

---

## `rules/ship.py`

Defines the `Ship` object.

Tracks:

* Ship name
* Size
* Occupied cells
* Damaged segments
* Shielded segments
* Stealth duration
* Ability state
* Remaining HP

---

## `rules/board.py`

Defines a player's board.

Handles:

* Ship placement
* Ship removal
* Bomb placement
* Incoming attacks
* Hit/miss resolution
* Shield blocks
* Stealth interactions
* Scans
* Relocation validation
* Repairable cells
* Shieldable cells
* Fleet-sunk detection

---

## `rules/extras.py`

Contains optional mechanics:

* Bomb
* Repair
* Shield

---

## `rules/game.py`

Controls the overall game state.

Handles:

* Current player
* Turns
* Attacks
* Ability usage
* Repair
* Shield
* Victory detection
* Action logs
* Player names
* Game options
* AI difficulty

This is the main rules-level interface used by the UI.

---

# AI Architecture

The computer opponent is split into separate difficulty modules.

```text
rules/ai.py
      │
      ├── ai_beginner.py
      ├── ai_intermediate.py
      └── ai_expert.py
```

`rules/ai.py` acts as the dispatcher.

The rest of the application can continue calling:

```python
ai_step(game)
```

without needing to know which difficulty implementation is active.

---

# UI Architecture

The Pygame interface is organized into screens.

```text
App
 │
 ├── MenuScreen
 │
 ├── SetupScreen
 │
 ├── HandoffScreen
 │
 ├── PlayScreen
 │
 └── GameOverScreen
```

Each screen has the standard lifecycle:

```text
enter()
on_event()
update()
draw()
```

`ui/app.py` owns the shared application state and controls screen switching.

---

# Audio

Audio is managed separately from the game rules.

```text
audio/
├── music.py
├── sfx.py
└── sound_manager.py
```

The current audio system provides:

* Background music
* Music looping
* Mute/unmute control
* Music cleanup when the application closes

`SoundManager` provides the interface used by the Pygame application.

---

# Documentation

The project documentation is divided into two main levels.

## `README.md`

This file provides:

* Project overview
* Installation
* Running instructions
* Gameplay overview
* Architecture
* Project structure
* Development guidance

## `docs/rules.md`

Contains the detailed rules reference.

Use it when you need the exact behavior of:

* Attacks
* Ships
* Abilities
* Optional mechanics
* Turns
* Deployment
* AI
* Victory conditions

---

# "Where Do I Change...?"

| I want to...                              | Go to                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| Change the board size                     | `rules/config.py`                                                                   |
| Change ship sizes                         | `rules/config.py`                                                                   |
| Change ability uses                       | `rules/config.py`                                                                   |
| Add/change ability cooldowns              | `rules/config.py`                                                                   |
| Change Recon size                         | `rules/config.py`                                                                   |
| Change Stealth duration                   | `rules/config.py`                                                                   |
| Change Repair uses                        | `rules/config.py`                                                                   |
| Change Shield uses                        | `rules/config.py`                                                                   |
| Change what Barrage does                  | `rules/abilities.py`                                                                |
| Change what Relocate does                 | `rules/abilities.py`                                                                |
| Change what Recon does                    | `rules/abilities.py`                                                                |
| Change what Row Scan does                 | `rules/abilities.py`                                                                |
| Change what Stealth does                  | `rules/abilities.py`                                                                |
| Add a new ship ability                    | `rules/config.py` + `rules/abilities.py` + `rules/game.py`/UI integration as needed |
| Change Bomb behavior                      | `rules/extras.py`                                                                   |
| Change Repair behavior                    | `rules/extras.py`                                                                   |
| Change Shield behavior                    | `rules/extras.py`                                                                   |
| Change hit/miss/stealth/shield resolution | `rules/board.py` → `receive_attack()`                                               |
| Change ship placement rules               | `rules/board.py`                                                                    |
| Change Relocate validation                | `rules/board.py` → `check_move()`                                                   |
| Change turn flow                          | `rules/game.py`                                                                     |
| Change attack count behavior              | `rules/game.py` and `rules/abilities.py`                                            |
| Change victory detection                  | `rules/game.py` / `rules/board.py`                                                  |
| Change Beginner AI                        | `rules/ai_beginner.py`                                                              |
| Change Intermediate AI                    | `rules/ai_intermediate.py`                                                          |
| Change Expert AI                          | `rules/ai_expert.py`                                                                |
| Change which AI difficulty is selected    | `rules/ai.py` / `ui/app.py`                                                         |
| Change default AI difficulty              | `ui/app.py`                                                                         |
| Change default optional mechanics         | `ui/app.py`                                                                         |
| Change game modes                         | `ui/app.py` / `ui/screens/menu.py`                                                  |
| Change deployment behavior                | `ui/screens/setup.py`                                                               |
| Change the battle screen                  | `ui/screens/play.py`                                                                |
| Change the game-over screen               | `ui/screens/gameover.py`                                                            |
| Change the handoff screen                 | `ui/screens/handoff.py`                                                             |
| Change screen navigation                  | `ui/app.py`                                                                         |
| Change colors                             | `ui/theme.py`                                                                       |
| Change fonts                              | `ui/theme.py`                                                                       |
| Move UI elements                          | `ui/layout.py` and the relevant screen                                              |
| Change board appearance                   | `ui/board_view.py`                                                                  |
| Change fleet-status panels                | `ui/panels.py`                                                                      |
| Change buttons/widgets                    | `ui/widgets.py`                                                                     |
| Change window/display settings            | `ui/display.py`                                                                     |
| Change background music behavior          | `audio/music.py`                                                                    |
| Change audio integration                  | `audio/sound_manager.py`                                                            |
| Add sound effects                         | `audio/sfx.py` + audio integration                                                  |
| Change general settings                   | `settings/settings.py`                                                              |

---

# Development Rule of Thumb

When changing the game, ask:

### Is this a rule?

Put it in:

```text
rules/
```

### Is this visual or input behavior?

Put it in:

```text
ui/
```

### Is this audio behavior?

Put it in:

```text
audio/
```

### Is this a tunable number?

Put it in:

```text
rules/config.py
```

Avoid putting game rules directly into Pygame screen code.

---

# Design Philosophy

WARGRID is structured around a separation between:

```text
GAME LOGIC
    ↓
rules/
    ↓
GAME STATE
    ↓
ui/
    ↓
VISUAL PRESENTATION
```

The goal is for the rules system to be understandable and testable without depending on Pygame.

The UI should present the game state and send player actions to the rules layer rather than deciding whether an action is legal.

---

# License

No license information is currently specified in the project files.
