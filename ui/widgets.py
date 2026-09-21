"""Reusable bits: text drawing and buttons."""
import pygame

from ui.display import screen
from ui.theme import ACCENT, MUTED, PANEL_2, SMALL, TEXT, FONT


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
