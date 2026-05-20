import pygame


class Projectile:
    def __init__(self, x, y, direction, screen):
        self.rect = pygame.Rect(x, y, 12, 8)
        self.screen = screen
        self.direction = direction
        self.speed = 7
        self.alive = True
        self.type = "Projectile"
        self.lifetime = 90

    def update(self, camera, entityList):
        if not self.alive:
            return
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False
            return
        self.rect.x += self.direction * self.speed
        for entity in entityList:
            if entity.alive and entity.alive is not None and entity.type == "Mob":
                if self.rect.colliderect(entity.rect):
                    entity.on_hit(self.direction)
                    self.alive = False
                    return
        pygame.draw.ellipse(
            self.screen,
            (255, 80, 0),
            (self.rect.x + camera.x, self.rect.y + camera.y,
             self.rect.width, self.rect.height),
        )
