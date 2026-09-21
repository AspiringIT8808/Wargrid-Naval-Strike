"""The window. Importing this module starts pygame and opens the window."""
import pygame

pygame.init()
W, H = 1280, 780
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("BATTLESHIPS // TACTICAL EDITION")
clock = pygame.time.Clock()
