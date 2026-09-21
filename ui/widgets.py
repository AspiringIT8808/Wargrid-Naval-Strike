"""Reusable bits: text drawing and buttons."""
import pygame

from ui.display import screen
from ui.theme import ACCENT, MUTED, PANEL_2, RED, SMALL, TEXT, FONT


def text(s, pos, font=FONT, color=TEXT, center=False):
    img = font.render(s, True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    screen.blit(img, rect)


class Button:
    def __init__(self, rect, label=""):
        self.rect = pygame.Rect(rect)
        self.label = label

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, enabled=True, selected=False, sub=None, label=None):
        over = enabled and self.rect.collidepoint(pygame.mouse.get_pos())
        fill = (32, 45, 60) if over else (PANEL_2 if enabled else (25, 28, 31))
        pygame.draw.rect(screen, fill, self.rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT if selected else (75, 95, 110), self.rect, 2, border_radius=6)
        color = TEXT if enabled else (95, 102, 108)
        label = label or self.label
        if sub is None:
            text(label, self.rect.center, SMALL, color, center=True)
        else:
            text(label, (self.rect.centerx, self.rect.y + 20), SMALL, color, center=True)
            text(sub, (self.rect.centerx, self.rect.y + 42), SMALL, MUTED if enabled else (80, 86, 92), center=True)


class MuteButton:
    def __init__(self, rect=(1216, 16, 44, 44)):
        self.rect = pygame.Rect(rect)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, muted=False):
        over = self.rect.collidepoint(pygame.mouse.get_pos())
        fill = (38, 52, 70) if over else PANEL_2
        border_col = ACCENT if not muted else (180, 80, 80)

        pygame.draw.rect(screen, fill, self.rect, border_radius=8)
        pygame.draw.rect(screen, border_col, self.rect, 2, border_radius=8)

        cx, cy = self.rect.centerx, self.rect.centery
        icon_color = TEXT if not muted else MUTED

        # Speaker body
        pygame.draw.rect(screen, icon_color, (cx - 11, cy - 4, 5, 8))
        pygame.draw.polygon(screen, icon_color, [(cx - 6, cy - 4), (cx + 1, cy - 9), (cx + 1, cy + 9), (cx - 6, cy + 4)])

        if not muted:
            # Sound waves
            pygame.draw.arc(screen, ACCENT, (cx - 1, cy - 6, 9, 12), -1.2, 1.2, 2)
            pygame.draw.arc(screen, ACCENT, (cx + 3, cy - 10, 12, 20), -1.2, 1.2, 2)
        else:
            # Red Mute X
            pygame.draw.line(screen, RED, (cx - 7, cy - 7), (cx + 9, cy + 9), 3)
            pygame.draw.line(screen, RED, (cx + 9, cy - 7), (cx - 7, cy + 9), 3)
