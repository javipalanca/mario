import json
import sys

import pygame


class SpriteSheet:
    def __init__(self, filename):
        # Cargar la imagen del sprite sheet
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

        self.width = 256 * 2
        self.height = 224 * 2
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Create a set for storing the pixels that have been processed
        self.processed = set()

    def flood_fill(self, x, y):
        # Get the width and height of the image
        width, height = self.sprite_sheet.get_size()

        # Create a queue for storing the pixels to process
        queue = [(x, y)]

        sprite_pixels = set()

        # Loop until the queue is empty
        while queue:
            # Get the next pixel to process
            x, y = queue.pop(0)

            # Skip this pixel if it has already been processed
            if (x, y) in self.processed:
                continue

            # Add this pixel to the processed set
            self.processed.add((x, y))

            # Check if the pixel is within the bounds of the image
            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            # Get the color of the pixel at position (x, y)
            color = self.sprite_sheet.get_at((x, y))

            # Check if the pixel is transparent
            if color.a == 0:
                continue

            # The pixel is non-transparent, so add it to the list
            sprite_pixels.add((x, y))

            # Add the neighboring pixels to the queue
            if (x + 1, y) not in queue:
                queue.append((x + 1, y))
            if (x - 1, y) not in queue:
                queue.append((x - 1, y))
            if (x, y + 1) not in queue:
                queue.append((x, y + 1))
            if (x, y - 1) not in queue:
                queue.append((x, y - 1))

        # Return the list of non-transparent pixels
        return sprite_pixels

    def get_sprites(self):
        sprites = {}
        # Recorrer la imagen del sprite sheet en busca de bordes de sprites
        for y in range(self.sprite_sheet.get_height()):
            for x in range(self.sprite_sheet.get_width()):
                # Obtener el color del pixel en la posición (x, y)
                color = self.sprite_sheet.get_at((x, y))

                # Si el color no es transparente, se ha encontrado un borde de sprite
                if color.a != 0 and (x, y) not in self.processed:
                    pixels = self.flood_fill(x, y)
                    xs, ys = zip(*pixels)
                    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
                    width, height = x1 - x0 + 1, y1 - y0 + 1
                    image = self.get_sprite(x0, y0, width, height)
                    self.draw_sprite(image, width, height)
                    name = self.input_text()
                    sprites[name] = {'x': x0, 'y': y0, 'w': width, 'h': height}

        return sprites

    def get_sprite(self, x0, y0, width, height):
        # Crear una imagen del sprite
        rect = pygame.Rect(x0, y0, width, height)
        image = self.sprite_sheet.subsurface(rect)
        return image

    def draw_sprite(self, image, width, height):
        image = pygame.transform.scale(image, (width * 8, height * 8))

        # Establecer la transparencia del sprite
        image.set_colorkey((0, 0, 255))

        self.screen.fill(pygame.Color(0, 0, 255))
        self.screen.blit(image, (0, 0))

        pygame.display.flip()

    def input_text(self):
        # Create a font object
        font = pygame.font.Font(None, 36)

        # Create an empty string to store the input text
        input_text = ""

        # Main game loop
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # Render the input text on the screen
            text_surface = font.render("Sprite: " + input_text, True, (255, 255, 255))

            # Draw the text on the screen
            pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), pygame.Rect(200, 100, 800, 30))
            self.screen.blit(text_surface, (200, 100))
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    ss = SpriteSheet("resources/graphics/smb_mario_sheet_clip.png")
    sprites = ss.get_sprites()
    with open("resources/sprites/mario_sheet.json", 'w') as f:
        json.dump(sprites, f)
