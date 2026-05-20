import pygame

from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


class HeavyBot(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound, dashboard):
        super().__init__(x, y - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("heavybot-1").image,
                self.spriteCollection.get("heavybot-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.collision = Collider(self, level)
        self.type = "Mob"
        self.hp = 2
        self.max_hp = 2
        self.dashboard = dashboard
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0)

    def update(self, camera):
        if self.alive is None:
            return

        if not self.alive:
            self._onDead(camera)
            return

        self.applyGravity()

        if self.hit_stun > 0:
            self.hit_stun -= 1
            self.rect.y += int(self.vel.y)
            self.collision.checkY()
            self.rect.x += int(self.knockback_vel)
            self.knockback_vel *= 0.8
            if self.hit_stun == 0 and self.hp <= 0:
                self.alive = False
                self.timer = 0
                self.textPos = Vec2D(self.rect.x + 3, self.rect.y)
                self.dashboard.points += 200
            if (self.hit_stun // 4) % 2 == 0:
                self._draw(camera)
            return

        self.leftrightTrait.update()
        self._draw(camera)
        self.animation.update()

    def _draw(self, camera):
        key = "heavybot-1" if self.hp >= 2 else "heavybot-damaged"
        frame = self.spriteCollection.get(key).image
        if self.leftrightTrait.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        self.screen.blit(frame, (self.rect.x + camera.x, self.rect.y - 32))

    def _onDead(self, camera):
        if self.timer < self.timeAfterDeath:
            self.textPos.y -= 0.5
            self.dashboard.drawText("200", self.textPos.x + camera.x, self.textPos.y, 8)
            frame = self.spriteCollection.get("heavybot-damaged").image
            self.screen.blit(frame, (self.rect.x + camera.x, self.rect.y - 32))
        else:
            self.alive = None
        self.timer += 0.1
