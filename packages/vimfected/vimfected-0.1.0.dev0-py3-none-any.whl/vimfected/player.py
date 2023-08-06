import pygame

from .utils import Point
from .sprites import sprites, PLAYER_DOWN, PLAYER_UP, PLAYER_LEFT, PLAYER_RIGHT
from .locals import TILE_SIZE

DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.location = Point(0, 0)
        self.sprites = {
            DOWN: sprites.get(PLAYER_DOWN),
            UP: sprites.get(PLAYER_UP),
            LEFT: sprites.get(PLAYER_LEFT),
            RIGHT: sprites.get(PLAYER_RIGHT),
        }
        self._set_sprite(DOWN)

    def handle(self, key):
        if key == pygame.K_j:
            self._move(DOWN)
            self._set_sprite(DOWN)
        elif key == pygame.K_k:
            self._move(UP)
            self._set_sprite(UP)
        elif key == pygame.K_h:
            self._move(LEFT)
            self._set_sprite(LEFT)
        elif key == pygame.K_l:
            self._move(RIGHT)
            self._set_sprite(RIGHT)

    def update(self):
        self.rect = pygame.Rect(
            (
                self.location.x * TILE_SIZE,
                self.location.y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
        )

    def _move(self, direction):
        self.location += direction

    def _set_sprite(self, key):
        self.surf = self.sprites[key]
        self.rect = self.surf.get_rect()
