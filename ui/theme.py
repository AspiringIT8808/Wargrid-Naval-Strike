"""Colors and fonts. Change the look of the whole game here."""
import pygame

pygame.font.init()

BG = (10, 15, 22)
PANEL_2 = (23, 32, 44)
GRID_C = (52, 72, 92)
WATER = (17, 42, 58)
TEXT = (225, 235, 242)
MUTED = (145, 160, 173)
ACCENT = (73, 207, 180)
RED = (230, 78, 92)
ORANGE = (239, 166, 70)
YELLOW = (244, 218, 102)
CYAN = (90, 200, 240)
WHITE = (245, 248, 250)
SHIP = (105, 118, 130)
SHIP_HIT = (175, 92, 80)
SHIP_SUNK = (95, 45, 50)
SHIP_STEALTH = (60, 92, 145)
SCAN_WATER = (24, 66, 74)
SCAN_SHIP = (98, 88, 40)

FONT = pygame.font.SysFont("consolas", 18)
SMALL = pygame.font.SysFont("consolas", 14)
BIG = pygame.font.SysFont("consolas", 28, bold=True)
HUGE = pygame.font.SysFont("consolas", 46, bold=True)
