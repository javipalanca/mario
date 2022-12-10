import json
from enum import Enum, auto

import pygame
from pygame import K_RIGHT, K_LEFT

from animation import Animation
from spritesheet import SpriteSheet

MAX_SPEED = 10
ACCELERATION = 0.2


class MarioState(Enum):
    IDLE = auto()
    WALK = auto()
    JUMP = auto()
    SWIM = auto()
    FLAG = auto()
    STOP = auto()
    DEAD = auto()


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()


class Mario(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        # self.image = pygame.image.load("resources/graphics/mario.png")
        # self.image = pygame.transform.scale(self.image, (26, 32))
        # self.rect = self.image.get_rect()
        self.speed = pygame.Vector2()
        self.speed.x, self.speed.y = 0, 0
        self.acceleration = pygame.Vector2()
        self.acceleration.x, self.acceleration.y = 0, 0
        self.direction = Direction.RIGHT
        self.state = MarioState.IDLE

        self.spritesheet = SpriteSheet("resources/graphics/smb_mario_sheet_clip.png")
        with open("resources/sprites/mario_sheet.json") as f:
            self.sprite_coords = json.load(f)

        self.animations = {
            Direction.LEFT: {
                MarioState.IDLE: Animation(self.spritesheet, self.sprite_coords, ["mario_idle"]),
                MarioState.WALK: Animation(self.spritesheet, self.sprite_coords, ["mario_walk1",
                                                                                  "mario_walk2",
                                                                                  "mario_walk3"]),
                MarioState.JUMP: Animation(self.spritesheet, self.sprite_coords, ["mario_jump"])
            },
            Direction.RIGHT: {
                MarioState.IDLE: Animation(self.spritesheet, self.sprite_coords, ["mario_idle"], flip=True),
                MarioState.WALK: Animation(self.spritesheet, self.sprite_coords, ["mario_walk1",
                                                                                  "mario_walk2",
                                                                                  "mario_walk3"], flip=True),
                MarioState.JUMP: Animation(self.spritesheet, self.sprite_coords, ["mario_jump"], flip=True)
            }
        }

        self.rect = self.get_rect()

        self.move(80, 368)

    def get_animation(self):
        return self.animations[self.direction][self.state]

    def get_rect(self):
        return self.get_animation().get_sprite().get_rect()

    def keydown_x(self, key):
        if key == K_RIGHT:
            self.acceleration.x = ACCELERATION
            self.direction = Direction.RIGHT
            self.state = MarioState.WALK
        elif key == K_LEFT:
            self.acceleration.x = -ACCELERATION
            self.direction = Direction.LEFT
            self.state = MarioState.WALK

    def keyup_x(self):
        self.acceleration.x = 0

    def update(self, clock):
        if self.acceleration.x == 0:
            self.speed.x = 0 if -0.1 < self.speed.x < 0.1 else self.speed.x * 0.7
        else:
            self.speed.x += self.acceleration.x
            self.speed.x = (
                min(self.speed.x, MAX_SPEED) if self.speed.x > 0 else max(self.speed.x, -MAX_SPEED)
            )

        self.move(self.speed.x, self.speed.y)
        # logger.debug(f"Mario:\trect: {self.rect}\tx,y: {self.rect.x},{self.rect.y}\tspeed: {self.speed}")
        if self.speed.x == 0:
            self.state = MarioState.IDLE
        self.get_animation().update(clock)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        if self.rect.x < 0:
            self.move_to(-self.rect.x, 0)

    def move_to(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def draw(self):
        self.screen.blit(self.get_animation().get_sprite(), self.rect)
