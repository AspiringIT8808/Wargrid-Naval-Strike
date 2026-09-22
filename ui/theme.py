"""Colors, fonts, and motion helpers. Change the look and feel of the whole game here."""
import math
import time

import pygame

pygame.font.init()

# ---------------------------------------------------------------- palette --
# Elevation tiers instead of one flat BG/PANEL pair -> panels visibly "float".
BG          = (8, 12, 18)          # deepest layer, behind everything
BG_GRADIENT_TOP = (10, 16, 24)
BG_GRADIENT_BOT = (6, 9, 14)
PANEL       = (17, 24, 34)         # a resting card
PANEL_2     = (23, 32, 44)         # kept for backward-compat with existing code
PANEL_RAISED = (27, 38, 52)        # a card that's "up" (selected/active)
PANEL_HOVER = (34, 47, 64)         # a card under the cursor

GRID_C = (46, 64, 84)
WATER  = (14, 36, 52)
WATER_DEEP = (10, 26, 38)

TEXT   = (232, 240, 246)
MUTED  = (128, 145, 160)
FAINT  = (70, 84, 98)              # for the quietest labels/dividers

# Two accents instead of one, so nothing has to multitask:
ACCENT       = (64, 217, 180)      # cyan-teal: selection, positive, "go"
ACCENT_DIM   = (40, 130, 112)
DANGER       = (235, 74, 90)       # hits, damage, destructive actions
DANGER_DIM   = (140, 50, 58)
WARNING      = (239, 166, 70)      # bomb, caution
GOLD         = (244, 200, 90)      # scans / discoveries

RED    = DANGER
ORANGE = WARNING
YELLOW = GOLD
CYAN   = (90, 205, 240)
WHITE  = (247, 250, 252)

SHIP         = (108, 122, 136)
SHIP_HIT     = (196, 92, 84)
SHIP_SUNK    = (70, 34, 38)
SHIP_STEALTH = (66, 100, 158)
SCAN_WATER   = (22, 64, 72)
SCAN_SHIP    = (108, 96, 44)

GLOW = (64, 217, 180)              # focus-ring / pulse color, pair with alpha

FONT  = pygame.font.SysFont("consolas", 18)
SMALL = pygame.font.SysFont("consolas", 14)
BIG   = pygame.font.SysFont("consolas", 28, bold=True)
HUGE  = pygame.font.SysFont("consolas", 46, bold=True)
LABEL = pygame.font.SysFont("consolas", 12, bold=True)   # tiny all-caps tags/badges


# ------------------------------------------------------------- easing ------
def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_out_back(t, overshoot=1.7):
    t = max(0.0, min(1.0, t))
    return 1 + (overshoot + 1) * (t - 1) ** 3 + overshoot * (t - 1) ** 2


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


# ------------------------------------------------------------- Anim --------
class Anim:
    """A single eased value that animates toward a target over `dur` seconds.
    Use for hover glow, button scale/punch, panel fade-ins, screen shake."""

    def __init__(self, value=0.0):
        self.value = value
        self._start = value
        self._target = value
        self._t0 = 0.0
        self._dur = 0.0
        self._ease = ease_out_cubic

    def to(self, target, dur=0.15, ease=ease_out_cubic):
        if target == self._target and self._dur:
            return self
        self._start, self._target = self.value, target
        self._t0, self._dur, self._ease = time.time(), dur, ease
        return self

    def update(self):
        if self._dur <= 0:
            self.value = self._target
            return self.value
        t = (time.time() - self._t0) / self._dur
        if t >= 1:
            self.value = self._target
            self._dur = 0
        else:
            self.value = lerp(self._start, self._target, self._ease(t))
        return self.value


class Shake:
    """Call kick() on impact, call offset() every frame while drawing the board."""

    def __init__(self):
        self.until = 0.0
        self.mag = 0.0

    def kick(self, mag=6, dur=0.18):
        self.until = time.time() + dur
        self.mag = mag
        self._dur = dur

    def offset(self):
        now = time.time()
        if now >= self.until:
            return 0, 0
        remaining = (self.until - now) / max(self._dur, 0.001)
        m = self.mag * remaining
        seed = now * 60
        return (math.sin(seed) * m, math.cos(seed * 1.3) * m)


def pulse(period=1.4, lo=0.35, hi=1.0):
    """0..1 breathing value for 'your turn' style ambient glow."""
    t = (math.sin(time.time() * (2 * math.pi / period)) + 1) / 2
    return lerp(lo, hi, t)


# --------------------------------------------------------- drawing helpers -
def vertical_gradient(surface, rect, top_color, bottom_color):
    x, y, w, h = rect
    for i in range(h):
        t = i / max(h - 1, 1)
        pygame.draw.line(surface, lerp_color(top_color, bottom_color, t), (x, y + i), (x + w, y + i))


def glow_rect(surface, rect, color, alpha, radius=10, spread=10):
    """Soft outer glow behind a panel/button — draw this BEFORE the panel itself."""
    glow = pygame.Surface((rect.width + spread * 2, rect.height + spread * 2), pygame.SRCALPHA)
    pygame.draw.rect(glow, (*color, alpha), glow.get_rect(), border_radius=radius + spread // 2)
    surface.blit(glow, (rect.x - spread, rect.y - spread))


def panel(surface, rect, fill=PANEL, border=FAINT, border_w=1, radius=10, shadow=True):
    """A 'card' with a soft drop shadow, replacing bare pygame.draw.rect panels."""
    if shadow:
        sh = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(sh, (0, 0, 0, 90), sh.get_rect(), border_radius=radius)
        surface.blit(sh, (rect.x, rect.y + 4))
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if border_w:
        pygame.draw.rect(surface, border, rect, border_w, border_radius=radius)
