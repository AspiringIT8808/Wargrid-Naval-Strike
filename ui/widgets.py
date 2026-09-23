"""Reusable bits: text drawing and buttons — now with hover glow, press punch,
and floating combat text so actions feel like they landed instead of just
changing a value silently."""
import time

import pygame

from ui.display import screen
from ui.theme import (ACCENT, DANGER, FAINT, FONT, GOLD, MUTED, PANEL, PANEL_HOVER,
                       PANEL_RAISED, RED, SMALL, TEXT, Anim, ease_out_back, glow_rect,
                       lerp_color, panel)


def text(s, pos, font=FONT, color=TEXT, center=False):
    img = font.render(s, True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    screen.blit(img, rect)


class Button:
    """Same call signature as before (hit / draw), but now animates:
    - hover: fill lightens, border glows, scales up 4%
    - press: punches down to 96% for a beat
    - disabled: no motion at all, so 'alive' buttons read as alive by contrast
    """

    def __init__(self, rect, label=""):
        self.rect = pygame.Rect(rect)
        self.label = label
        self._hover = Anim(0.0)
        self._press_until = 0.0

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def punch(self):
        """Call this from on_event when the button is actually clicked/activated."""
        self._press_until = time.time() + 0.09

    def draw(self, enabled=True, selected=False, sub=None, label=None):
        over = enabled and self.rect.collidepoint(pygame.mouse.get_pos())
        self._hover.to(1.0 if over else 0.0, dur=0.12)
        h = self._hover.update()

        pressed = time.time() < self._press_until
        scale = 0.96 if pressed else (1.0 + 0.04 * h)
        r = self.rect
        w, hgt = int(r.width * scale), int(r.height * scale)
        draw_rect = pygame.Rect(0, 0, w, hgt)
        draw_rect.center = r.center

        fill = lerp_color(PANEL if enabled else (20, 24, 29), PANEL_HOVER, h)
        if selected:
            fill = PANEL_RAISED
        border_col = ACCENT if selected else lerp_color((70, 88, 104), ACCENT, h)

        if (selected or h > 0.05) and enabled:
            glow_rect(screen, draw_rect, ACCENT, alpha=int(50 * max(h, 0.6 if selected else 0)), spread=8)

        panel(screen, draw_rect, fill=fill, border=border_col,
              border_w=2 if (selected or over) else 1, radius=7, shadow=enabled)

        color = TEXT if enabled else (95, 102, 108)
        label = label or self.label
        if sub is None:
            text(label, draw_rect.center, SMALL, color, center=True)
        else:
            text(label, (draw_rect.centerx, draw_rect.y + 20), SMALL, color, center=True)
            text(sub, (draw_rect.centerx, draw_rect.y + 42), SMALL,
                 MUTED if enabled else (80, 86, 92), center=True)


class MuteButton:
    def __init__(self, rect=(1216, 16, 44, 44)):
        self.rect = pygame.Rect(rect)
        self._hover = Anim(0.0)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, muted=False):
        over = self.rect.collidepoint(pygame.mouse.get_pos())
        self._hover.to(1.0 if over else 0.0, dur=0.12)
        h = self._hover.update()

        fill = lerp_color(PANEL, PANEL_HOVER, h)
        border_col = ACCENT if not muted else (180, 80, 80)
        panel(screen, self.rect, fill=fill, border=border_col, border_w=2, radius=8)

        cx, cy = self.rect.centerx, self.rect.centery
        icon_color = TEXT if not muted else MUTED

        pygame.draw.rect(screen, icon_color, (cx - 11, cy - 4, 5, 8))
        pygame.draw.polygon(screen, icon_color, [(cx - 6, cy - 4), (cx + 1, cy - 9),
                                                   (cx + 1, cy + 9), (cx - 6, cy + 4)])
        if not muted:
            pygame.draw.arc(screen, ACCENT, (cx - 1, cy - 6, 9, 12), -1.2, 1.2, 2)
            pygame.draw.arc(screen, ACCENT, (cx + 3, cy - 10, 12, 20), -1.2, 1.2, 2)
        else:
            pygame.draw.line(screen, RED, (cx - 7, cy - 7), (cx + 9, cy + 9), 3)
            pygame.draw.line(screen, RED, (cx + 9, cy - 7), (cx - 7, cy + 9), 3)


class FloatingText:
    """One drifting, fading label — spawn on hit/miss/ability so the player
    SEES the consequence of a click instead of just noticing a cell changed."""

    def __init__(self, txt, pos, color=TEXT, life=2.5, rise=45, font=SMALL):
        self.txt, self.pos0, self.color, self.life, self.rise, self.font = txt, pos, color, life, rise, font
        self.t0 = time.time()

    @property
    def dead(self):
        return time.time() - self.t0 > self.life

    def draw(self):
        t = min(1.0, (time.time() - self.t0) / self.life)
        y = self.pos0[1] - self.rise * ease_out_back(t, overshoot=0.6)
        alpha = int(255 * (1 - t))
        img = self.font.render(self.txt, True, self.color)
        img.set_alpha(alpha)
        rect = img.get_rect(center=(self.pos0[0], y))
        screen.blit(img, rect)


class FloatingTextLayer:
    """Owns a list of FloatingText; screens keep one instance and call
    update_and_draw() once per frame after the board is drawn."""

    def __init__(self):
        self.items = []

    def spawn(self, txt, pos, color=TEXT, **kw):
        self.items.append(FloatingText(txt, pos, color, **kw))

    def update_and_draw(self):
        self.items = [f for f in self.items if not f.dead]
        for f in self.items:
            f.draw()
