import pygame


class Level:
    def __init__(self, screen):
        self.background_image = pygame.image.load("resources/graphics/level_1.png")
        self.background_image = pygame.transform.scale2x(self.background_image)
        self.background_image = self.background_image.convert()

        self.background_rect = self.background_image.get_rect()
        self.screen = screen
        self.viewport = self.screen.get_rect()  # bottom=self.background_rect.bottom)

    def update(self, clock, mario):
        if mario.rect.right > (self.viewport.right - self.viewport.left)/2:
            # Move the background to the right
            self.background_rect.move_ip(-mario.speed.x, 0)
            # Move the viewport to the right
            mario.move(-mario.speed.x, 0)

    def draw(self):
        self.screen.blit(self.background_image, self.background_rect)  # (0, 0), self.viewport)
        # pygame.draw.rect(self.screen, pygame.Color(255, 0, 0), self.viewport, 1)
