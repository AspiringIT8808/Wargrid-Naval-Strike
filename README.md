# Battleships: Tactical Edition

    pip install -r requirements.txt
    py main.py

## Project map

```
main.py                 start here (just launches the app)
rules/                  THE GAME RULES -- never imports pygame
  config.py             every tunable number: ship sizes, uses, cooldowns, recon size...
  grid.py               (row, col) helpers: in_bounds, cell_name, line_cells, area_cells
  abilities.py          the Ability class (uses/cooldown) + what each ship ability DOES
  ship.py               Ship: cells, damage, shields, stealth
  board.py              one player's board: placement, incoming shots, scans, bomb cell
  extras.py             optional mechanics: Bomb, Repair, Shield
  game.py               Game: turns, attack(), use_ability(), use_repair(), use_shield()
  ai.py                 the computer opponent
ui/                     EVERYTHING PYGAME
  display.py            window + clock
  theme.py              colors and fonts
  layout.py             sizes and pixel positions
  widgets.py            text() and Button
  board_view.py         drawing boards, markers, hover highlights, pixel <-> cell
  panels.py             the fleet-status column between the boards
  app.py                shared state + main loop + switching screens
  screens/
    base.py             the 4 hooks every screen has: enter / on_event / update / draw
    menu.py             title, optional-mechanic toggles, choose mode
    setup.py            placing ships and the bomb
    handoff.py          "pass the device" curtain (2-player mode)
    play.py             the battle: clicks -> Game actions, action buttons, previews
    gameover.py         win/lose overlay
```

The rule of the house: **`rules/` decides, `ui/` shows.** The UI never changes ships or boards
directly; it calls `Game.attack / use_ability / use_repair / use_shield` and draws the result.

## "Where do I change...?"

| I want to...                                   | Go to                                  |
|------------------------------------------------|----------------------------------------|
| change ship size, ability uses, cooldowns      | `rules/config.py`                      |
| change what an ability does                    | `rules/abilities.py` (one function each) |
| add a new ship ability                         | `config.py` (new spec) + `abilities.py` (new function + dict entry) + a button in `ui/screens/play.py` |
| change Bomb / Repair / Shield                  | `rules/extras.py`                      |
| change how a shot resolves (hit/miss/stealth)  | `rules/board.py` -> `receive_attack`   |
| change turn order or win condition             | `rules/game.py`                        |
| make the computer smarter                      | `rules/ai.py`                          |
| change colors / fonts                          | `ui/theme.py`                          |
| move things around on screen                   | `ui/layout.py` (boards), the screen's own file (buttons) |
| change how boards / ships / markers look       | `ui/board_view.py`                     |
| change the battle screen                       | `ui/screens/play.py`                   |
| add a new screen                               | new file in `ui/screens/` + one line in `ui/app.py` |
