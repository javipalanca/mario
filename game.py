import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT, KEYUP

from level import Level
from mario import Mario


class Game:
    def __init__(self):
        self.running = False
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.width = 256 * 2
        self.height = 224 * 2
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.level = Level(self.screen)
        self.mario = Mario(self.screen)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key in (K_RIGHT, K_LEFT):
                        self.mario.keydown_x(event.key)
                elif event.type == KEYUP:
                    if event.key in (K_RIGHT, K_LEFT):
                        self.mario.keyup_x()

            self.mario.update(self.clock)
            self.level.update(self.clock, self.mario)
            self.level.draw()
            self.mario.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)
