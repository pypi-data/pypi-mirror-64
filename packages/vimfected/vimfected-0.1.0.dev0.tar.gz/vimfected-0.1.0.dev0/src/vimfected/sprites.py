import pygame

from .locals import COLOR_KEY, TILE_SIZE
from .utils import asset_path

# Sprite names (as tile coordinates on the sprite sheet)
PLAYER_DOWN = (0, 0)
PLAYER_RIGHT = (1, 0)
PLAYER_UP = (2, 0)
PLAYER_LEFT = (3, 0)


class SpriteSheet:
    def __init__(self):
        self.sheet = pygame.image.load(asset_path("tiles.png"))

    def get(self, tile):
        x, y = tile
        return self.image_at(x, y)

    def image_at(self, x, y):
        coords = (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        rect = pygame.Rect(coords)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(COLOR_KEY, pygame.RLEACCEL)
        return image


sprites = SpriteSheet()
