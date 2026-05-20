from copy import copy

from entities.EntityBase import EntityBase


class PowerBox(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, sound, dashboard, level, gravity=0):
        super().__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.type = "Block"
        self.triggered = False
        self.spawned = False
        self.time = 0
        self.maxTime = 10
        self.sound = sound
        self.dashboard = dashboard
        self.level = level
        self.vel_anim = 1
        self.animation = copy(self.spriteCollection.get("CoinBox").animation)

    def update(self, cam):
        if self.alive and not self.triggered:
            self.animation.update()
        else:
            self.animation.image = self.spriteCollection.get("empty").image
            if self.triggered and not self.spawned:
                self.level.addWeaponPowerup(self.rect.x // 32, self.rect.y // 32 - 1)
                self.spawned = True
            if self.time < self.maxTime:
                self.time += 1
                self.rect.y -= self.vel_anim
            else:
                if self.time < self.maxTime * 2:
                    self.time += 1
                    self.rect.y += self.vel_anim
        self.screen.blit(
            self.spriteCollection.get("sky").image,
            (self.rect.x + cam.x, self.rect.y + 2),
        )
        self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y - 1))
