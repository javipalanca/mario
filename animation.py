from itertools import cycle
from loguru import logger
import pygame

MIN_FRAMES = 2


class Animation:
    def __init__(self, spritesheet, coords, frame_names, flip=False):
        self.flip = flip
        self.last_animation = 0
        self.animated = len(frame_names) > 0
        self.frames = self.extract_frames(spritesheet, coords, frame_names)
        self.current_frame = next(self.frames)

    def extract_frames(self, spritesheet, coords, frame_names):
        frames = []
        for name in frame_names:
            info = coords[name]
            frame = spritesheet.get_sprite(info['x'], info['y'], info['w'], info['h'])
            frame = pygame.transform.scale2x(frame)
            if self.flip:
                frame = pygame.transform.flip(frame, flip_x=True, flip_y=False)
            frames.append(frame)
        return cycle(frames)

    def update(self, clock):
        if self.animated:
            self.last_animation += 1
            if self.last_animation > MIN_FRAMES:
                self.last_animation = 0
                self.current_frame = next(self.frames)

    def get_sprite(self):
        return self.current_frame
