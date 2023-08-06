import pygame

from .player import Player


SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200
FRAMES_PER_SECOND = 30


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            self._update()
            self._render()
            self.clock.tick(FRAMES_PER_SECOND)

        pygame.quit()

    def _render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player.surf, self.player.rect)
        pygame.display.flip()

    def _update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.player.handle(event.key)

        self.player.update()


def main():
    game = Game()
    game.run()
