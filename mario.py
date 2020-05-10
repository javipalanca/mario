import pygame
from pygame.locals import QUIT, K_RIGHT, K_ESCAPE, KEYDOWN, KEYUP, K_LEFT


class Mario(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("resources/graphics/mario.png")
        self.image = pygame.transform.scale(self.image, (26, 32))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 368)
        self.speed = pygame.Vector2()
        self.speed.x, self.speed.y = 0, 0
        self.acceleration = pygame.Vector2()
        self.acceleration.x, self.acceleration.y = 0, 0

    def keydown_x(self, key):
        if key == K_RIGHT:
            self.acceleration.x = 0.2
        elif key == K_LEFT:
            self.acceleration.x = -0.2

    def keyup_x(self):
        self.acceleration.x = 0

    def update(self):
        if self.acceleration.x == 0:
            self.speed.x = 0 if -0.01 < self.speed.x < 0.01 else self.speed.x * 0.9
        else:
            self.speed.x += self.acceleration.x
            self.speed.x = (
                min(self.speed.x, 20) if self.speed.x > 0 else max(self.speed.x, -20)
            )

        self.rect.move_ip(self.speed)
        print(f"rect: {self.rect}\tspeed: {self.speed}")

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Level:
    def __init__(self, screen):
        self.image = pygame.image.load("resources/graphics/level_1.png")
        self.image = pygame.transform.scale2x(self.image)
        self.image = self.image.convert()

        self.rect = self.image.get_rect()
        self.screen = screen
        self.viewport = self.screen.get_rect(bottom=self.rect.bottom)

    def update(self, mario):
        self.viewport.center = mario.rect.center
        self.viewport.clamp_ip(self.rect)
        print(
            f"Viewport: {self.viewport}\tcenter: {self.viewport.center[0]}\tmario: {mario.rect.center[0]}"
        )

    def draw(self):
        self.screen.blit(self.image, (0, 0), self.viewport)


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

            self.mario.update()
            self.level.update(self.mario)
            self.level.draw()
            self.mario.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    game.run()
