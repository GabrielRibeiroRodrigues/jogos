import pygame
from pygame.transform import flip

from classes.Animation import Animation
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait


class Drone(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound, dashboard):
        super().__init__(x, y - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("drone-1").image,
                self.spriteCollection.get("drone-2").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.collision = Collider(self, level)
        self.type = "Mob"
        self.hp = 1
        self.max_hp = 1
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
                self.dashboard.points += 100
            if (self.hit_stun // 4) % 2 == 0:
                self._draw(camera)
            return

        self.leftrightTrait.update()
        self._draw(camera)
        self.animation.update()

    def _draw(self, camera):
        frame = self.animation.image
        if self.leftrightTrait.direction == -1:
            frame = flip(frame, True, False)
        self.screen.blit(frame, (self.rect.x + camera.x - 16, self.rect.y - 32))

    def _onDead(self, camera):
        if self.timer < self.timeAfterDeath:
            self.textPos.y -= 0.5
            self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8)
            self.screen.blit(
                self.spriteCollection.get("drone-flat").image,
                (self.rect.x + camera.x - 16, self.rect.y - 32),
            )
        else:
            self.alive = None
        self.timer += 0.1
