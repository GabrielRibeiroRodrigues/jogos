import pygame


class Projectile:
    def __init__(self, x, y, direction, screen):
        self.rect = pygame.Rect(x, y, 14, 5)
        self.screen = screen
        self.direction = direction
        self.speed = 9
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

        rx = self.rect.x + camera.x
        ry = self.rect.y

        # rastro laranja
        pygame.draw.rect(self.screen, (180, 80, 0),
                         (rx - self.direction * 8, ry + 1, 8, 3))
        # núcleo amarelo brilhante
        pygame.draw.rect(self.screen, (255, 240, 60),
                         (rx, ry, self.rect.width, self.rect.height))
        # ponta branca
        tip_x = rx + self.rect.width if self.direction == 1 else rx - 2
        pygame.draw.rect(self.screen, (255, 255, 200), (tip_x, ry + 1, 3, 3))
