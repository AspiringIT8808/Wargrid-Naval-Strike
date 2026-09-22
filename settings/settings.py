"""ESC menu configuration.

This file is ONLY for the in-game ESC Settings menu.

Bomb / Repair / Shield are gameplay options
and do NOT belong here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SettingsConfig:

    # -------------------------
    # Text
    # -------------------------

    title: str = "SETTINGS"

    back_label: str = "BACK TO GAME"
    restart_label: str = "RESTART LEVEL"
    menu_label: str = "MAIN MENU"

    esc_hint: str = "ESC = Back to Game"
    controls_label: str = "1 BACK   2 RESTART   3 MAIN MENU"

    # -------------------------
    # Text positions
    # -------------------------

    title_y: int = 145
    hint_y: int = 490
    controls_y: int = 525

    # -------------------------
    # Overlay
    # -------------------------

    overlay_alpha: int = 190


SETTINGS = SettingsConfig()