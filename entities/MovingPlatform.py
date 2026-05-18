import pygame


class MovingPlatform:
    def __init__(self, x, y, level, screen, direction="horizontal", amplitude=3, speed=1):
        # x, y in TILE coords (multiply by 32 for pixels)
        # direction: "horizontal" or "vertical"
        # amplitude: tiles to move (e.g. 3 = moves 3 tiles left/right)
        # speed: pixels per frame (e.g. 1.5)
        self.alive = True
        self.type = "Platform"
        self.rect = pygame.Rect(x * 32, y * 32, 64, 16)  # 2 tiles wide, half tile tall platform
        self.screen = screen
        self.level = level
        self.direction = direction
        self.amplitude = amplitude * 32  # convert to pixels
        self.speed = speed
        self.startX = x * 32
        self.startY = y * 32
        self.vel = speed  # current velocity, flips when reaching amplitude
        self.image = self._loadSprite()
        self.collisionRect = self.rect.copy()

    def _loadSprite(self):
        try:
            sheet = pygame.image.load("./img/tiles.png").convert()
            tile = pygame.Surface((16, 16))
            tile.blit(sheet, (0, 0), pygame.Rect(4 * 16, 4 * 16, 16, 16))
            return pygame.transform.scale(tile, (64, 16))
        except Exception:
            surf = pygame.Surface((64, 16))
            surf.fill((82, 96, 124))  # stone gray color
            return surf

    def update(self, camera):
        # Move the platform
        if self.direction == "horizontal":
            self.rect.x += self.vel
            if abs(self.rect.x - self.startX) >= self.amplitude:
                self.vel *= -1
        else:  # vertical
            self.rect.y += self.vel
            if abs(self.rect.y - self.startY) >= self.amplitude:
                self.vel *= -1
        self.collisionRect = self.rect.copy()
        self.draw(camera)

    def draw(self, camera):
        drawX = self.rect.x + camera.x
        drawY = self.rect.y + camera.y
        self.screen.blit(self.image, (drawX, drawY))
