import pygame


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None, ignoreTileSize=False,
                 xTileSize=16, yTileSize=16):
        if ignoreTileSize:
            rect = pygame.Rect((x, y, xTileSize, yTileSize))
        else:
            rect = pygame.Rect((x * xTileSize, y * yTileSize, xTileSize, yTileSize))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = self.sheet.get_at((rect.x, rect.y))[:3]
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (int(xTileSize * scalingfactor), int(yTileSize * scalingfactor))
        )
